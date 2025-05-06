import pynvml
import logging

logger = logging.getLogger(__name__)

class NvmlWrapper:
    def __init__(self):
        try:
            pynvml.nvmlInit()
            self.device_count = pynvml.nvmlDeviceGetCount()
            logger.info(f"Initialized NVML with {self.device_count} devices")
            self.handles = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.device_count)]
        except pynvml.NVMLError as e:
            logger.error(f"Failed to initialize NVML: {e}")
            self.device_count = 0
            self.handles = []

        # Defensive check to ensure collect_metrics method exists
        if not hasattr(self, 'collect_metrics'):
            logger.error("NvmlWrapper instance missing 'collect_metrics' method after initialization")

    def get_device_handles(self):
        return self.handles

    def get_power_usage(self, handle):
        try:
            # Power usage in milliwatts
            # Some GPUs may not support power usage query, handle that gracefully
            power_mw = pynvml.nvmlDeviceGetPowerUsage(handle)
            if power_mw == 0:
                # Sometimes zero means unsupported or unavailable
                logger.warning("Power usage returned zero, may be unsupported on this device")
                return None
            return power_mw / 1000.0  # Convert to watts
        except pynvml.NVMLError_FunctionNotFound:
            logger.error("Power usage function not found on this device")
            return None
        except pynvml.NVMLError as e:
            logger.error(f"Failed to get power usage: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to get power usage: {type(e).__name__}: {e}")
            return None

    def get_temperature(self, handle):
        try:
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            return temp
        except pynvml.NVMLError as e:
            logger.error(f"Failed to get temperature: {e}")
            return None

    def get_clock_speed(self, handle):
        try:
            clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
            return clock
        except pynvml.NVMLError as e:
            logger.error(f"Failed to get clock speed: {e}")
            return None

    def collect_metrics(self):
        metrics = []
        for handle in self.handles:
            power = self.get_power_usage(handle)
            temp = self.get_temperature(handle)
            clock = self.get_clock_speed(handle)
            metrics.append({
                'power': power,
                'temperature': temp,
                'clock': clock
            })
        return metrics

    def shutdown(self):
        try:
            pynvml.nvmlShutdown()
            logger.info("NVML shutdown successfully")
        except pynvml.NVMLError as e:
            logger.error(f"Failed to shutdown NVML: {e}")
