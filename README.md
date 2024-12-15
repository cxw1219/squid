# Squid - OANDA Data Synchronization

## Supported Instruments
- Major Forex Pairs (EUR/USD, GBP/USD, USD/JPY, etc.)
- Gold (XAU/USD)
- SPX500_USD

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
- SQLite storage with optimized indexing
- Live status display

## Recent Updates
- Added XAU_USD (Gold) tracking
- Fixed database transaction handling
- Improved error recovery