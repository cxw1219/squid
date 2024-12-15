# Squid - OANDA Data Synchronization

## Latest Status
- Fully functional with historical data collection
- Priority-based instrument ordering
- Enhanced status display with types and progress
- Stable database operations

## Features
- Historical data download (up to 4 years)
- Real-time synchronization
- Priority ordering: Metals > Forex > Bonds > Indices
- SQLite storage with transaction safety
- Live status display with progress tracking

## Instrument Types
- METAL-1: XAU_USD
- FOREX-2: Major currency pairs
- BOND-3: Treasury instruments
- INDEX-4: Stock indices

## Performance
- 20,000 candles per instrument
- Parallel processing with 8 workers
- Optimized chunk sizes
- Transaction batching

## Status Display
- Real-time progress tracking
- Instrument type labeling
- Price and spread monitoring
- Download progress percentage

## Recent Fixes
- Improved database transaction handling
- Fixed progress tracking
- Enhanced error recovery
- Better type handling for instruments