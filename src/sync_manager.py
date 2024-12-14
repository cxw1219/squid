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

    def run(self):
        logging.info("Starting OANDA data sync")
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                while self.running:
                    current_time = datetime.now(pytz.UTC)
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
                    time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Received interrupt signal")
        finally:
            self.running = False
            logging.info("Shutdown complete")