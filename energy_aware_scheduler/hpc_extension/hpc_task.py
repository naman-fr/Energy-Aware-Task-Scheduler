class HPCTask:
    def __init__(self, task_id, computation_profile=None, communication_pattern=None):
        self.task_id = task_id
        self.computation_profile = computation_profile or {}
        self.communication_pattern = communication_pattern or {}
        self.scalability_profile = None
        self.memory_footprint = None

    def set_computation_profile(self, profile):
        self.computation_profile = profile

    def set_communication_pattern(self, pattern):
        self.communication_pattern = pattern

    def set_scalability_profile(self, scalability):
        self.scalability_profile = scalability

    def set_memory_footprint(self, memory):
        self.memory_footprint = memory
