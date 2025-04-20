from prometheus_client import start_http_server, Gauge
import threading
import time
from energy_aware_scheduler.k8s_plugin.telemetry_integration import TelemetryIntegration
import logging

logger = logging.getLogger(__name__)

class PrometheusExporter:
    def __init__(self, port=8000):
        self.telemetry = TelemetryIntegration()
        self.power_gauge = Gauge('node_power_watts', 'Power usage of node in watts', ['node'])
        self.temp_gauge = Gauge('node_temperature_celsius', 'Temperature of node in Celsius', ['node'])
        self.score_gauge = Gauge('node_score', 'Scheduling score of node', ['node'])
        self.port = port
        self.running = False

    def update_metrics(self):
        while self.running:
            for i in range(len(self.telemetry.handles)):
                telemetry_data = self.telemetry.get_node_telemetry(i)
                if telemetry_data:
                    node_label = f"node_{i}"
                    power = telemetry_data.get('power', 0)
                    temp = telemetry_data.get('temperature', 0)
                    # For score, use a simple weighted sum as example
                    score = 0.7 * power + 0.3 * temp
                    self.power_gauge.labels(node=node_label).set(power)
                    self.temp_gauge.labels(node=node_label).set(temp)
                    self.score_gauge.labels(node=node_label).set(score)
            time.sleep(5)

    def start(self):
        start_http_server(self.port)
        self.running = True
        thread = threading.Thread(target=self.update_metrics)
        thread.daemon = True
        thread.start()
        logger.info(f"Prometheus exporter started on port {self.port}")

    def stop(self):
        self.running = False
        self.telemetry.shutdown()
