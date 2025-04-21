import threading
import time
from energy_aware_scheduler.simulator.simulator import EnergyAwareSimulator
from energy_aware_scheduler.simulator.node import Node
from energy_aware_scheduler.simulator.job import Job

class DigitalTwin:
    def __init__(self, real_scheduler_interface, update_interval=5.0):
        self.real_scheduler = real_scheduler_interface
        self.update_interval = update_interval
        self.sim_env = None  # simpy.Environment() in real setup
        self.nodes = []
        self.simulator = None
        self.running = False
        self.thread = threading.Thread(target=self.run)

    def initialize_simulator(self):
        # Initialize nodes and simulator state from real scheduler
        real_nodes = self.real_scheduler.get_nodes()
        self.nodes = [Node(n.node_id, n.cpu_count, n.gpu_count) for n in real_nodes]
        self.simulator = EnergyAwareSimulator(self.sim_env, self.nodes)

    def start(self):
        self.running = True
        self.initialize_simulator()
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        while self.running:
            # Sync state from real scheduler
            jobs = self.real_scheduler.get_active_jobs()
            # Update simulator jobs accordingly
            for job in jobs:
                sim_job = Job(job.job_id, job.workload_type, job.average_power, job.duration)
                self.simulator.submit_job(sim_job)
            # Advance simulation time
            # self.sim_env.step() or similar in real setup
            time.sleep(self.update_interval)
            # Optionally refine model parameters based on real telemetry
