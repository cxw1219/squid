#!/usr/bin/env python3
import logging
import sys
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Add the project root directory to Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from src.sync_manager import OandaSync
from src.exceptions import SecurityError, DatabaseError

def setup_logging():
    log_dir = Path(ROOT_DIR) / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler = RotatingFileHandler(
        log_dir / 'oanda_sync.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

def check_config():
    config_path = Path(ROOT_DIR) / 'config' / 'config.ini'
    if not config_path.exists():
        raise FileNotFoundError(
            f"\nERROR: Configuration file not found at {config_path}\n"
            "Please copy config.example.ini to config.ini and fill in your OANDA credentials."
        )

    data_dir = Path(ROOT_DIR) / 'data'
    data_dir.mkdir(exist_ok=True)
    
    test_file = data_dir / '.write_test'
    try:
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        raise PermissionError(f"Data directory {data_dir} is not writable: {e}")

    return str(config_path)

def main():
    try:
        setup_logging()
        logging.info("Starting OANDA data synchronization")
        
        config_path = check_config()
        logging.info(f"Using configuration from: {config_path}")
        
        syncer = OandaSync(config_path=config_path)
        syncer.run()

    except FileNotFoundError as e:
        logging.error(f"Configuration error: {e}")
        print(f"\nERROR: {str(e)}")
        sys.exit(1)
    except SecurityError as e:
        logging.error(f"Security error: {e}")
        print(f"\nSecurity Error: Please check your OANDA credentials")
        sys.exit(1)
    except DatabaseError as e:
        logging.error(f"Database error: {e}")
        print(f"\nDatabase Error: Please check your database configuration and permissions")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Received keyboard interrupt, shutting down gracefully...")
        print("\nShutting down gracefully...")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nERROR: An unexpected error occurred. Check logs for details.")
        sys.exit(1)
    finally:
        logging.info("Shutdown complete")

if __name__ == "__main__":
    main()