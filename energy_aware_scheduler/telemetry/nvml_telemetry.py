import threading
import time
import logging
from energy_aware_scheduler.telemetry.nvml_wrapper import NvmlWrapper

logger = logging.getLogger(__name__)

class AsyncNvmlTelemetry:
    def __init__(self, poll_interval=1.0):
        self.nvml = NvmlWrapper()
        self.poll_interval = poll_interval
        self.running = False
        self.data_buffer = []
        self.thread = threading.Thread(target=self._poll_loop)

    def start(self):
        self.running = True
        self.thread.start()
        logger.info("Async NVML telemetry started.")

    def stop(self):
        self.running = False
        self.thread.join()
        logger.info("Async NVML telemetry stopped.")

    def _poll_loop(self):
        while self.running:
            try:
                logger.debug(f"Polling NVML metrics from object: {self.nvml}, attributes: {dir(self.nvml)}")
                if not hasattr(self.nvml, 'collect_metrics'):
                    logger.error("NvmlWrapper instance missing 'collect_metrics' method")
                    time.sleep(self.poll_interval)
                    continue
                data = self.nvml.collect_metrics()
                self.data_buffer.append(data)
            except Exception as e:
                logger.error(f"Error collecting NVML metrics: {e}")
            time.sleep(self.poll_interval)

    def get_latest_data(self):
        if self.data_buffer:
            return self.data_buffer[-1]
        return None
