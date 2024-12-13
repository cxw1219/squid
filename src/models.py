from dataclasses import dataclass
from pathlib import Path

@dataclass
class OandaConfig:
    api_token: str
    account_id: str
    environment: str
    database_path: Path
    max_retries: int = 3
    retry_delay: int = 60
    rate_limit_delay: float = 0.1
    batch_size: int = 5000
    sync_interval: int = 3600
    price_decimal_places: int = 5
    datetime_format: str = '%Y-%m-%dT%H:%M:%SZ'
    audit_log_path: Path = Path('audit.log')