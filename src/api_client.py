import time
import logging
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
from datetime import datetime, timedelta
import backoff
from typing import Optional, List, Dict

from .exceptions import SecurityError, RateLimitExceeded, DataIntegrityError

class OandaAPIClient:
    def __init__(self, access_token: str, environment: str = 'practice'):
        self._validate_credentials(access_token)
        self.client = oandapyV20.API(
            access_token=access_token,
            environment=environment
        )
        self.last_request_time = 0
        self.MIN_REQUEST_INTERVAL = 0.1