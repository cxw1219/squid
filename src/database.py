import sqlite3
import logging
from contextlib import contextmanager
from datetime import datetime
import pandas as pd
import pytz
from pathlib import Path
from .exceptions import DatabaseError

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._initialize_database()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            conn.close()

    def _initialize_database(self):
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS oanda_prices (
                        instrument TEXT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        open REAL NOT NULL,
                        high REAL NOT NULL,
                        low REAL NOT NULL,
                        close REAL NOT NULL,
                        volume INTEGER NOT NULL,
                        complete BOOLEAN NOT NULL,
                        spread REAL,
                        validation_hash TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (instrument, timestamp)
                    )
                """)
                conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON oanda_prices(timestamp)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_instrument_time ON oanda_prices(instrument, timestamp)")
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS audit_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        operation TEXT NOT NULL,
                        details TEXT,
                        status TEXT
                    )
                """)
        except Exception as e:
            raise DatabaseError(f"Database initialization failed: {str(e)}")

    def log_audit(self, operation: str, details: str, status: str = "completed"):
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO audit_log (operation, details, status)
                    VALUES (?, ?, ?)
                """, (operation, details, status))
        except Exception as e:
            logging.error(f"Error logging audit: {e}")

    def get_last_timestamp(self, instrument: str) -> datetime:
        try:
            with self.get_connection() as conn:
                row = conn.execute(
                    "SELECT MAX(timestamp) as last_sync FROM oanda_prices WHERE instrument = ?",
                    (instrument,)
                ).fetchone()
                if row and row['last_sync']:
                    return datetime.fromisoformat(row['last_sync'])
                return datetime.now(pytz.UTC) - timedelta(days=1)
        except Exception as e:
            logging.error(f"Error getting last timestamp: {e}")
            raise DatabaseError(str(e))

    def save_candles(self, df: pd.DataFrame):
        if df.empty:
            return
        try:
            with self.get_connection() as conn:
                df.to_sql('oanda_prices', conn, if_exists='append', 
                         index=False, method='multi', chunksize=1000)
        except Exception as e:
            logging.error(f"Error saving candles: {e}")
            raise DatabaseError(str(e))