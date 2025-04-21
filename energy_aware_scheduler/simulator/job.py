class Job:
    def __init__(self, job_id, workload_type, average_power, duration):
        self.job_id = job_id
        self.workload_type = workload_type
        self.average_power = average_power
        self.duration = duration
        self.remaining_time = duration
        self.start_time = None
        self.end_time = None
        self.assigned_node = None
        self.completed = False

    def run(self, time_interval):
        if self.remaining_time > 0:
            self.remaining_time -= time_interval
            if self.remaining_time <= 0:
                self.remaining_time = 0
                self.completed = True

    def is_complete(self):
        return self.completed
