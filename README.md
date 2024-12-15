# Squid - OANDA Data Synchronization

## Performance Optimizations
- Increased chunk size to optimal 13.89 hours (5000 candles at S10)
- Parallel processing with 8 workers
- Reduced rate limit delay to 0.01 seconds
- Batch processing for candles and database operations
- Compression headers for API requests
- Transaction batching for database operations

## Features
- Historical data download (up to 4 years)
- Real-time synchronization
- Multiple currency pairs and SPX500_USD
- SQLite storage with optimized indexing
- Live status display

## Configuration
See config.example.ini for optimized settings.

## Usage
1. Copy config.example.ini to config.ini
2. Add your OANDA credentials
3. Run main.py

## Performance
- Optimized for OANDA's 5000 candle limit
- Efficient batch processing
- Database transaction optimization