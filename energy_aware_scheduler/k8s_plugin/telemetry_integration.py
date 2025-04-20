from energy_aware_scheduler.telemetry.nvml_wrapper import NvmlWrapper
import logging

logger = logging.getLogger(__name__)

class TelemetryIntegration:
    def __init__(self):
        self.nvml = NvmlWrapper()
        self.handles = self.nvml.get_device_handles()

    def get_node_telemetry(self, node_index=0):
        """
        Get telemetry data for a node (GPU device) by index.
        Returns a dict with power (W), temperature (C), and clock speed (MHz).
        """
        if node_index >= len(self.handles):
            logger.error(f"Node index {node_index} out of range")
            return None
        handle = self.handles[node_index]
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
        self.nvml.shutdown()
