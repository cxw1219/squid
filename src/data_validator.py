import logging
from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict
import hashlib
import pytz

from .exceptions import DataValidationError, PriceIntegrityError

class DataValidator:
    @staticmethod
    def validate_price_data(df: pd.DataFrame) -> bool:
        if df.empty:
            return True

        if df.isnull().any().any():
            raise DataValidationError("Missing values detected in price data")

        invalid_prices = (
            (df['high'] < df['low']) |
            (df['open'] > df['high']) |
            (df['open'] < df['low']) |
            (df['close'] > df['high']) |
            (df['close'] < df['low'])
        )
        
        if invalid_prices.any():
            raise PriceIntegrityError(f"Invalid price relationships detected")