import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class Node:
    def __init__(self, node_id: str, cpu_count: int, gpu_count: int, nvidia_ai_chip_count: int = 0, thermal_capacity: float = 100.0, fan_curve: Optional[Dict[float, float]] = None):
        self.node_id = node_id
        self.cpu_count = cpu_count
        self.gpu_count = gpu_count
        self.nvidia_ai_chip_count = nvidia_ai_chip_count
        self.thermal_capacity = thermal_capacity
        self.fan_curve = fan_curve or {}
        self.current_temperature = 25.0  # Ambient temperature in Celsius
        self.fan_speed = 0.0  # Current fan speed percentage
        self.current_power = 0.0  # Current power draw in watts

    def update_temperature(self, power_draw: float, time_interval: float):
        """
        Update the node's temperature based on power draw and time interval.
        This is a simplified thermal model using thermal capacity and fan cooling effect.
        """
        temperature_rise = power_draw * time_interval / self.thermal_capacity
        cooling_effect = self.fan_speed * 0.1 * time_interval  # Cooling proportional to fan speed and time
        self.current_temperature += temperature_rise - cooling_effect
        if self.current_temperature < 25.0:
            self.current_temperature = 25.0  # Ambient temperature floor
        self.fan_speed = self.get_fan_speed()
        logger.debug(f"Node {self.node_id} temperature updated by {temperature_rise:.2f}C, cooled by {cooling_effect:.2f}C to {self.current_temperature:.2f}C, fan speed set to {self.fan_speed:.1f}%")

    def get_fan_speed(self) -> float:
        """
        Get the fan speed based on the current temperature using the fan curve.
        Fan curve is a dict mapping temperature to fan speed percentage.
        """
        if not self.fan_curve:
            return 0.0
        temperatures = sorted(self.fan_curve.keys())
        for temp in temperatures:
            if self.current_temperature < temp:
                return self.fan_curve[temp]
        return self.fan_curve[temperatures[-1]]
