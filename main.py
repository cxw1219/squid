import logging
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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