from energy_aware_scheduler.telemetry.nvml_wrapper import NvmlWrapper
from energy_aware_scheduler.telemetry.nvml_telemetry import AsyncNvmlTelemetry
import logging

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

    def shutdown(self):
        self.async_telemetry.stop()
        self.nvml.shutdown()
