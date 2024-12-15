import time
import logging
from datetime import datetime
from typing import Optional, List, Dict
import backoff
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import pytz

from .exceptions import SecurityError, RateLimitExceeded, DataIntegrityError

class OandaAPIClient:
    def __init__(self, access_token: str, environment: str = 'practice'):
        if not self._validate_credentials(access_token):
            raise SecurityError("Invalid API token format")
            
        self.client = oandapyV20.API(
            access_token=access_token,
            environment=environment
        )
        self.last_request_time = 0
        self.MIN_REQUEST_INTERVAL = 0.01  # Reduced to 10ms

    def _validate_credentials(self, token: str) -> bool:
        if not token or len(token) < 10:
            return False
        return True

    @backoff.on_exception(
        backoff.expo,
        (oandapyV20.exceptions.V20Error, RateLimitExceeded),
        max_tries=5,
        max_time=300
    )
    def make_request(self, request):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.MIN_REQUEST_INTERVAL:
            time.sleep(self.MIN_REQUEST_INTERVAL - time_since_last_request)
        
        try:
            response = self.client.request(request)
            self.last_request_time = time.time()
            return response
        except oandapyV20.exceptions.V20Error as e:
            if hasattr(e, 'code'):
                if e.code == 'TOO_MANY_REQUESTS':
                    raise RateLimitExceeded(str(e))
                elif e.code in ['INSTRUMENT_NOT_FOUND', 'PRICE_NOT_FOUND']:
                    logging.error(f"OANDA API Error: {e.code} - {str(e)}")
                    return None
            raise

    def validate_account(self, account_id: str) -> bool:
        try:
            r = accounts.AccountSummary(accountID=account_id)
            self.make_request(r)
            logging.info("Account validation successful")
            return True
        except Exception as e:
            logging.error(f"Account validation failed: {e}")
            raise

    def fetch_candles(self, instrument: str, start_time: datetime, end_time: datetime,
                     granularity: str = "S10", price: str = "MBA") -> Optional[List[Dict]]:
        params = {
            "granularity": granularity,
            "from": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "to": end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "price": price,
            "alignmentTimezone": "UTC",
            "count": 5000
        }

        try:
            logging.info(f"Requesting {instrument} data from {start_time} to {end_time}")
            r = instruments.InstrumentsCandles(instrument=instrument, params=params)
            
            headers = {
                'Accept-Encoding': 'gzip',
                'Accept-Datetime-Format': 'RFC3339'
            }
            r.headers = headers
            
            response = self.make_request(r)
            
            if not response or 'candles' not in response:
                raise DataIntegrityError("Invalid response format from OANDA")
            
            candles = response['candles']
            logging.info(f"Received {len(candles)} candles for {instrument}")
                
            return candles
        except Exception as e:
            logging.error(f"Error fetching candles for {instrument}: {e}")
            raise