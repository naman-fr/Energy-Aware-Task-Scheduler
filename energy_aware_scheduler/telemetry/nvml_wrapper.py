import pynvml
import logging

logger = logging.getLogger(__name__)

class NvmlWrapper:
    def __init__(self):
        try:
            pynvml.nvmlInit()
            self.device_count = pynvml.nvmlDeviceGetCount()
            logger.info(f"Initialized NVML with {self.device_count} devices")
        except pynvml.NVMLError as e:
            logger.error(f"Failed to initialize NVML: {e}")
            self.device_count = 0

    def get_device_handles(self):
        handles = []
        for i in range(self.device_count):
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                handles.append(handle)
            except pynvml.NVMLError as e:
                logger.error(f"Failed to get handle for device {i}: {e}")
        return handles

    def get_power_usage(self, handle):
        try:
            # Power usage in milliwatts
            power_mw = pynvml.nvmlDeviceGetPowerUsage(handle)
            return power_mw / 1000.0  # Convert to watts
        except pynvml.NVMLError as e:
            logger.error(f"Failed to get power usage: {e}")
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

    def shutdown(self):
        try:
            pynvml.nvmlShutdown()
            logger.info("NVML shutdown successfully")
        except pynvml.NVMLError as e:
            logger.error(f"Failed to shutdown NVML: {e}")
