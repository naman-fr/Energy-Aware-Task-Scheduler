import threading
import time
import psutil
import logging

logger = logging.getLogger(__name__)

class CpuTelemetry:
    def __init__(self, poll_interval=1.0):
        self.poll_interval = poll_interval
        self.running = False
        self.data_buffer = []
        self.thread = threading.Thread(target=self._poll_loop)

    def start(self):
        self.running = True
        self.thread.start()
        logger.info("CPU telemetry started.")

    def stop(self):
        self.running = False
        self.thread.join()
        logger.info("CPU telemetry stopped.")

    def _poll_loop(self):
        while self.running:
            try:
                cpu_percent = psutil.cpu_percent(interval=None)
                cpu_freq = psutil.cpu_freq()
                data = {
                    "cpu_percent": cpu_percent,
                    "cpu_freq_current": cpu_freq.current if cpu_freq else None,
                    "cpu_freq_min": cpu_freq.min if cpu_freq else None,
                    "cpu_freq_max": cpu_freq.max if cpu_freq else None,
                    "timestamp": time.time()
                }
                self.data_buffer.append(data)
            except Exception as e:
                logger.error(f"Error collecting CPU metrics: {e}")
            time.sleep(self.poll_interval)

    def get_latest_data(self):
        if self.data_buffer:
            return self.data_buffer[-1]
        return None
