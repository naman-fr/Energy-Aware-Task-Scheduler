import numpy as np

class AlgorithmComparator:
    def __init__(self, system_model):
        self.system_model = system_model
        self.algorithms = {
            "Fair Share": self.fair_share,
            "Green Scheduling": self.green_scheduling,
            "Thermal-Aware": self.thermal_aware,
        }

    def fair_share(self, tasks):
        # Simple fair share scheduling based on user quotas
        schedule = {}
        for task in tasks:
            schedule[task.task_id] = self.system_model.get_available_resources()[0]
        return schedule

    def green_scheduling(self, tasks):
        # Schedule tasks to nodes with highest renewable energy percentage
        schedule = {}
        nodes = self.system_model.get_available_resources()
        renewable_scores = {node.node_id: self.system_model.get_renewable_energy_percentage(node) for node in nodes}
        sorted_nodes = sorted(nodes, key=lambda n: renewable_scores[n.node_id], reverse=True)
        for i, task in enumerate(tasks):
            schedule[task.task_id] = sorted_nodes[i % len(sorted_nodes)]
        return schedule

    def thermal_aware(self, tasks):
        # Schedule tasks to nodes with lowest temperature
        schedule = {}
        nodes = self.system_model.get_available_resources()
        sorted_nodes = sorted(nodes, key=lambda n: n.current_temperature)
        for i, task in enumerate(tasks):
            schedule[task.task_id] = sorted_nodes[i % len(sorted_nodes)]
        return schedule

    def compare_algorithms(self, tasks):
        results = {}
        for name, algo in self.algorithms.items():
            schedule = algo(tasks)
            energy = self.estimate_energy(schedule)
            avg_temp = self.estimate_avg_temperature(schedule)
            results[name] = {
                "schedule": schedule,
                "energyConsumption": energy,
                "avgTemp": avg_temp,
            }
        return results

    def estimate_energy(self, schedule):
        # Placeholder: sum of estimated energy per task allocation
        total_energy = 0
        for task_id, node in schedule.items():
            total_energy += self.system_model.predict_energy_consumption(task_id, node)
        return total_energy

    def estimate_avg_temperature(self, schedule):
        # Placeholder: average temperature of nodes in schedule
        temps = [node.current_temperature for node in schedule.values()]
        return np.mean(temps) if temps else 0
