import configparser
import logging
import os
import signal
from datetime import datetime, timedelta
from pathlib import Path
import time
import pytz
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import RotatingFileHandler

from .models import OandaConfig
from .api_client import OandaAPIClient
from .data_validator import DataValidator
from .database import DatabaseManager
from .exceptions import (
    SecurityError,
    RateLimitExceeded,
    DataIntegrityError,
    DatabaseError
)

class OandaSync:
    def __init__(self, config_path: str = 'config.ini'):
        """Initialize the OandaSync class"""
        self.config = self._load_config(config_path)
        self.api_client = OandaAPIClient(
            access_token=self.config.api_token,
            environment=self.config.environment
        )
        self.instruments = [
            "EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", 
            "USD_CAD", "USD_CHF", "NZD_USD", "EUR_GBP"
        ]
        self.data_validator = DataValidator()
        self.db_manager = DatabaseManager(self.config.database_path)
        self._setup_logging()
        self._setup_signal_handlers()
        self.running = True
        self._validate_account()

    def _load_config(self, config_path: str) -> OandaConfig:
        """Load configuration from INI file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        config = configparser.ConfigParser()
        config.read(config_path)

        try:
            return OandaConfig(
                api_token=config['OANDA']['api_token'],
                account_id=config['OANDA']['account_id'],
                environment=config['OANDA']['environment'],
                database_path=Path(config['Paths']['database_path']),
                max_retries=config.getint('Settings', 'max_retries', fallback=3),
                retry_delay=config.getint('Settings', 'retry_delay', fallback=60),
                rate_limit_delay=config.getfloat('Settings', 'rate_limit_delay', fallback=0.1),
                batch_size=config.getint('Settings', 'batch_size', fallback=5000)
            )
        except KeyError as e:
            raise ValueError(f"Missing required configuration: {e}")

    def _setup_logging(self):
        """Configure rotating file logger"""
        log_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = RotatingFileHandler(
            'oanda_sync.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(log_formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    def _setup_signal_handlers(self):
        """Setup handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logging.info(f"Received signal {signum}. Initiating graceful shutdown...")
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _validate_account(self):
        """Validate OANDA account credentials"""
        try:
            self.api_client.validate_account(self.config.account_id)
            logging.info("Account validation successful")
        except Exception as e:
            logging.error(f"Account validation failed: {e}")
            raise

    def _should_sync_now(self, instrument: str) -> bool:
        """Determine if synchronization should occur"""
        current_time = datetime.now(pytz.UTC)
        
        # Skip weekends
        if current_time.weekday() >= 5:
            logging.info(f"Skipping weekend sync for {instrument}")
            return False
            
        # Get last sync time
        last_sync = self.db_manager.get_last_timestamp(instrument)
        time_since_sync = (current_time - last_sync).total_seconds()
        
        return time_since_sync >= self.config.sync_interval

    def sync_instrument(self, instrument: str):
        """Sync single instrument data with enhanced validation"""
        try:
            if not self._should_sync_now(instrument):
                return

            last_timestamp = self.db_manager.get_last_timestamp(instrument)
            current_time = datetime.now(pytz.UTC)

            # Round down to the nearest hour
            sync_time = last_timestamp.replace(
                minute=0, second=0, microsecond=0
            )

            candles = self.api_client.fetch_candles(instrument, sync_time, self.config)
            if candles:
                for candle in candles:
                    if not self.data_validator.validate_candle(candle):
                        continue
                        
                    # Process and save valid candles
                    df = self._process_candle_data(candle, instrument)
                    if not df.empty:
                        self.db_manager.save_candles(df)
                        
                logging.info(f"Completed sync for {instrument}")

        except RateLimitExceeded:
            logging.warning(f"Rate limit hit for {instrument}")
            time.sleep(self.config.retry_delay)
        except Exception as e:
            logging.error(f"Error syncing {instrument}: {e}")
            self.db_manager.log_audit("sync_failure", f"{instrument}: {str(e)}")
            raise

    def _process_candle_data(self, candle: dict, instrument: str):
        """Process a single candle into DataFrame format"""
        try:
            data = [{
                'instrument': instrument,
                'timestamp': pd.to_datetime(candle['time']),
                'open': float(candle['mid']['o']),
                'high': float(candle['mid']['h']),
                'low': float(candle['mid']['l']),
                'close': float(candle['mid']['c']),
                'volume': int(candle['volume']),
                'complete': True,
                'spread': float(candle['ask']['c']) - float(candle['bid']['c'])
            }]
            
            df = pd.DataFrame(data)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert('UTC')
                self.data_validator.validate_price_data(df)
                self.data_validator.validate_timestamps(df)
            
            return df
        except Exception as e:
            logging.error(f"Error processing candle data: {e}")
            return pd.DataFrame()

    def run(self):
        """Main execution loop with enhanced error handling"""
        logging.info("Starting OANDA data sync")
        
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                while self.running:
                    current_time = datetime.now(pytz.UTC)
                    
                    # Only sync on the hour
                    if current_time.minute == 0:
                        futures = [
                            executor.submit(self.sync_instrument, instrument)
                            for instrument in self.instruments
                        ]
                        
                        for future in futures:
                            try:
                                future.result()
                            except Exception as e:
                                logging.error(f"Error in sync task: {e}")
                    
                    # Sleep until next check (every minute)
                    time.sleep(60)
                    
        except KeyboardInterrupt:
            logging.info("Received interrupt signal")
        finally:
            self.running = False
            self.db_manager.log_audit("shutdown", "system", "Normal shutdown")
            logging.info("Shutdown complete")
