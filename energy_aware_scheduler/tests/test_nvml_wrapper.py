import pytest
from energy_aware_scheduler.telemetry.nvml_wrapper import NvmlWrapper

def test_nvml_initialization():
    nvml = NvmlWrapper()
    assert nvml.device_count >= 0
    nvml.shutdown()

def test_nvml_device_handles():
    nvml = NvmlWrapper()
    handles = nvml.get_device_handles()
    assert isinstance(handles, list)
    nvml.shutdown()

def test_nvml_power_temperature_clock():
    nvml = NvmlWrapper()
    handles = nvml.get_device_handles()
    for handle in handles:
        power = nvml.get_power_usage(handle)
        temp = nvml.get_temperature(handle)
        clock = nvml.get_clock_speed(handle)
        assert power is None or power >= 0
        assert temp is None or (0 <= temp <= 150)
        assert clock is None or clock >= 0
    nvml.shutdown()
