from energy_aware_scheduler.telemetry.nvml_wrapper import NvmlWrapper
from energy_aware_scheduler.telemetry.nvml_telemetry import AsyncNvmlTelemetry
import logging
from energy_aware_scheduler.k8s_plugin.server import anfis_detector, mmt_migrator, ecc_encryptor, nodes

logger = logging.getLogger(__name__)

class TelemetryIntegration:
    def __init__(self):
        self.nvml = NvmlWrapper()
        self.async_telemetry = AsyncNvmlTelemetry()
        self.async_telemetry.start()

    def get_node_telemetry(self, node_index=0):
        if node_index >= len(self.nvml.get_device_handles()):
            logger.error(f"Node index {node_index} out of range")
            return None
        # Return latest async telemetry data if available
        latest_data = self.async_telemetry.get_latest_data()
        if latest_data:
            return latest_data
        # Fallback to synchronous telemetry
        handle = self.nvml.get_device_handles()[node_index]
        power = self.nvml.get_power_usage(handle)
        temperature = self.nvml.get_temperature(handle)
        clock = self.nvml.get_clock_speed(handle)
        telemetry = {
            'power': power,
            'temperature': temperature,
            'clock': clock
        }
        logger.debug(f"Telemetry for node {node_index}: {telemetry}")
        return telemetry

    def get_host_utilization_metrics(self):
        metrics = []
        for node in nodes:
            cpu_util = getattr(node, 'cpu_utilization', 0.0)
            mem_util = getattr(node, 'memory_utilization', 0.0)
            metrics.append({
                "host_id": node.node_id,
                "cpu_util": cpu_util,
                "mem_util": mem_util,
                "over_utilized": False,
            })
        # Use ANFIS to detect over-utilized hosts
        over_utilized_indices = anfis_detector.detect_over_utilized_hosts(metrics)
        for idx in over_utilized_indices:
            metrics[idx]["over_utilized"] = True
        return metrics

    def get_migration_status(self):
        # Placeholder: return current VM migration status
        # This can be extended to track actual migrations
        return {
            "migrations_in_progress": 0,
            "last_migration_time": None,
        }

    def get_encryption_status(self):
        # Placeholder: return ECC encryption status or metrics
        return {
            "encryption_enabled": True,
            "last_encryption_time": None,
        }

    def telemetry_summary(self):
        host_metrics = self.get_host_utilization_metrics()
        migration_status = self.get_migration_status()
        encryption_status = self.get_encryption_status()
        summary = {
            "host_utilization": host_metrics,
            "migration_status": migration_status,
            "encryption_status": encryption_status,
        }
        return summary

    def shutdown(self):
        self.async_telemetry.stop()
        self.nvml.shutdown()
