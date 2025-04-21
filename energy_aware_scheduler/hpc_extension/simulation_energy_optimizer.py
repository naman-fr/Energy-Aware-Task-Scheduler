class SimulationEnergyOptimizer:
    def optimize(self, simulation_task):
        phases = simulation_task.decompose_phases()
        for phase in phases:
            if phase.is_io_intensive():
                phase.set_cpu_frequency_scaling("minimum")
            elif phase.is_communication_intensive():
                phase.set_network_config("high_bandwidth")
