import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Job:
    def __init__(self, job_id: str, workload_type: str, average_power: float, duration: float):
        self.job_id = job_id
        self.workload_type = workload_type
        self.average_power = average_power  # Average power draw in watts
        self.duration = duration  # Duration in seconds
        self.remaining_time = duration

    def run(self, time_interval: float):
        """
        Simulate running the job for a given time interval.
        """
        self.remaining_time = max(0.0, self.remaining_time - time_interval)
        logger.debug(f"Job {self.job_id} ran for {time_interval}s, remaining time {self.remaining_time}s")

    def is_complete(self) -> bool:
        return self.remaining_time <= 0.0
