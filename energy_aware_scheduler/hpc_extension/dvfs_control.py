import pynvml
import logging

logger = logging.getLogger(__name__)

class DVFSController:
    def __init__(self):
        pynvml.nvmlInit()
        self.device_count = pynvml.nvmlDeviceGetCount()

    def set_gpu_clock(self, device_index, graphics_clock, memory_clock):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(device_index)
            pynvml.nvmlDeviceSetApplicationsClocks(handle, memory_clock, graphics_clock)
            logger.info(f"Set GPU {device_index} clocks: graphics={graphics_clock} MHz, memory={memory_clock} MHz")
        except pynvml.NVMLError as e:
            logger.error(f"Failed to set GPU clocks for device {device_index}: {e}")

    def reset_gpu_clock(self, device_index):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(device_index)
            pynvml.nvmlDeviceResetApplicationsClocks(handle)
            logger.info(f"Reset GPU {device_index} clocks to default")
        except pynvml.NVMLError as e:
            logger.error(f"Failed to reset GPU clocks for device {device_index}: {e}")

    def shutdown(self):
        pynvml.nvmlShutdown()
