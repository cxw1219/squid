# Squid - OANDA Data Sync Tool

A robust Python tool for synchronizing OANDA forex data with SQLite storage, featuring advanced data validation and integrity checks.

## Features

- Downloads OANDA forex data with 10-second granularity
- Stores data in SQLite database for efficient querying
- Implements comprehensive data validation
- Handles rate limiting and API best practices
- Provides audit logging and data integrity checks
- Supports multiple currency pairs
- Hourly synchronization with error handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cxw1219/squid.git
cd squid
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create config file:
Copy `config/config.example.ini` to `config/config.ini` and fill in your OANDA credentials:
```ini
[OANDA]
api_token = your_api_token_here
account_id = your_account_id_here
environment = practice

[Paths]
database_path = data/oanda.db

[Settings]
max_retries = 3
retry_delay = 60
rate_limit_delay = 0.1
batch_size = 5000
sync_interval = 3600
```

## Usage

Run the synchronization tool:
```bash
python main.py
```

## Project Structure

```
oanda_sync/
│
├── config/
│   ├── __init__.py
│   └── config.ini
│
├── src/
│   ├── __init__.py
│   ├── models.py         # Data classes
│   ├── api_client.py     # OANDA API interaction
│   ├── data_validator.py # Data validation
│   ├── database.py      # Database operations
│   ├── exceptions.py    # Custom exceptions
│   ├── sync_manager.py  # Main sync logic
│   └── utils.py         # Utility functions
│
├── requirements.txt
├── README.md
└── main.py
```

## Features in Detail

### Data Validation
- Price relationship validation (high > low, etc.)
- Timestamp integrity checks
- Outlier detection
- Missing value handling

### Security
- Secure API token handling
- Data integrity hashing
- Audit logging
- Secure database connections

### Performance
- Batch database operations
- Connection pooling
- Efficient data structures
- Index optimization

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OANDA for providing the API
- Contributors and maintainers
