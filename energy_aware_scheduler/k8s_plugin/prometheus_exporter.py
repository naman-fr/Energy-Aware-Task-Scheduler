from prometheus_client import start_http_server, Gauge
import threading
import time
import logging
from energy_aware_scheduler.telemetry.nvml_telemetry import NvmlTelemetry

logger = logging.getLogger(__name__)

class PrometheusExporter:
    def __init__(self, port=8000):
        self.port = port
        self.nvml_telemetry = NvmlTelemetry()
        self.gpu_power_gauge = Gauge('gpu_power_watts', 'GPU Power Usage in Watts', ['device'])
        self.gpu_temp_gauge = Gauge('gpu_temperature_celsius', 'GPU Temperature in Celsius', ['device'])
        self.gpu_clock_gauge = Gauge('gpu_clock_mhz', 'GPU Clock Speed in MHz', ['device'])
        self.running = False

    def start(self):
        start_http_server(self.port)
        self.running = True
        thread = threading.Thread(target=self.update_metrics_loop)
        thread.daemon = True
        thread.start()
        logger.info(f"Prometheus exporter started on port {self.port}")

    def update_metrics_loop(self):
        while self.running:
            try:
                samples = self.nvml_telemetry.sample_all_devices()
                for sample in samples:
                    device = str(sample['device_index'])
                    power = sample.get('power_watts', 0)
                    temp = sample.get('temperature_celsius', 0)
                    clock = sample.get('clock_mhz', 0)
                    self.gpu_power_gauge.labels(device=device).set(power)
                    self.gpu_temp_gauge.labels(device=device).set(temp)
                    self.gpu_clock_gauge.labels(device=device).set(clock)
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error updating Prometheus metrics: {e}")

    def stop(self):
        self.running = False
        self.nvml_telemetry.shutdown()

if __name__ == "__main__":
    exporter = PrometheusExporter()
    exporter.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exporter.stop()
