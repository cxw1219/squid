# Squid - OANDA Data Syncing Tool

High-performance historical and real-time data synchronization tool for OANDA forex and CFD data.

## Features

- Downloads up to 4 years of historical data at 10-second resolution
- Supports multiple currency pairs and SPX500_USD
- Efficient batch processing with automatic rate limiting
- Real-time data synchronization
- SQLite storage with optimized indexes
- Comprehensive data validation
- Live status display

## Supported Instruments

- Major Forex Pairs (EUR/USD, GBP/USD, USD/JPY, etc.)
- SPX500_USD (S&P 500 CFD)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cxw1219/squid.git
cd squid
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure:
```bash
cp config/config.example.ini config/config.ini
# Edit config.ini with your OANDA credentials
```

## Configuration

Example configuration:
```ini
[OANDA]
api_token = your_api_token_here
account_id = your_account_id_here
environment = practice

[Paths]
database_path = data/oanda.db

[Settings]
historical_days = 1460  # 4 years
granularity = S10      # 10-second intervals
backfill_enabled = true
max_workers = 4
```

## Usage

Run the sync tool:
```bash
python main.py
```

## Data Structure

Data is stored in SQLite with the following schema:
- instrument (TEXT)
- timestamp (DATETIME)
- open (REAL)
- high (REAL)
- low (REAL)
- close (REAL)
- volume (INTEGER)
- spread (REAL)

## Features

### Historical Data
- Downloads up to 4 years of historical data
- Efficient chunked downloading
- Automatic rate limit handling
- Progress tracking
- Data validation

### Real-time Sync
- Hourly updates
- Live status display
- Automatic error recovery
- Rate limit management

### Validation
- Price relationship checks
- Data integrity verification
- Missing data detection
- Market hours validation for SPX500

## License

MIT License

## Note

SPX500_USD data follows market hours and may have wider spreads than forex pairs.