class PowerBudgetManager:
    def __init__(self, total_power_budget):
        self.total_budget = total_power_budget
        self.allocated_power = 0
        self.tasks_power_allocation = {}

    def allocate_power(self, task, requested_power):
        if self.allocated_power + requested_power > self.total_budget:
            return self._negotiate_power(task, requested_power)
        else:
            self.allocated_power += requested_power
            self.tasks_power_allocation[task.task_id] = requested_power
            return requested_power

    def _negotiate_power(self, task, requested_power):
        # Simplified negotiation: allocate remaining power proportionally
        remaining_power = self.total_budget - self.allocated_power
        allocated = min(requested_power, remaining_power)
        self.allocated_power += allocated
        self.tasks_power_allocation[task.task_id] = allocated
        return allocated
