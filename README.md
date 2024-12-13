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
Copy `config/config.example.ini` to `config/config.ini` and fill in your OANDA credentials.

## Usage

Run the synchronization tool:
```bash
python main.py
```

## Project Structure

See documentation for full project structure and features.