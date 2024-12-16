
    def sync_instrument(self, instrument: str):
        """Sync single instrument data with optimized batch processing"""
        try:
            if not self._should_sync_now(instrument):
                self.sync_status.update(instrument, "skipped", "Not due for sync")
                return

            logging.info(f"Starting sync for {instrument}")
            self.sync_status.update(instrument, "running", "Analyzing data range...")

            # Get data range and create chunks
            start_time, end_time = self._get_historical_range(instrument)
            chunks = self._calculate_historical_chunks(start_time, end_time, instrument)  # Fixed line
            total_chunks = len(chunks)

            self.sync_status.set_progress(instrument, 0, total_chunks)
            logging.info(f"Syncing {instrument} from {start_time} to {end_time}")
