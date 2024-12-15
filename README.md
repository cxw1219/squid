# Squid - OANDA Data Synchronization

## Latest Updates
- Added prioritized instrument display
- Improved status display with instrument types
- Priority order: Metals > Forex > Bonds > Indices

## Features
- Historical and real-time data synchronization
- Priority-based data collection
- Enhanced status display with instrument types
- SQLite storage with transaction batching
- Multi-threaded operation

## Status Display
The live status display now shows:
- Instrument priority levels
- Real-time sync progress
- Current prices and spreads
- Operation status

## Priorities
1. Precious Metals (METAL-1): XAU_USD
2. Forex Pairs (FOREX-2): Major currency pairs
3. Bonds (BOND-3): Treasury instruments
4. Indices (INDEX-4): Stock indices