import logging
import sys
from src.sync_manager import OandaSync

def main():
    try:
        config_path = "config/config.ini"
        syncer = OandaSync(config_path=config_path)
        syncer.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()