import simpy
import logging
from typing import List, Optional
from .node import Node
from .job import Job

logger = logging.getLogger(__name__)

class EnergyAwareSimulator:
    def __init__(self, env: simpy.Environment, nodes: List[Node]):
        self.env = env
        self.nodes = nodes
        self.jobs_queue: List[Job] = []
        self.running_jobs = {}

    def submit_job(self, job: Job):
        logger.info(f"Job {job.job_id} submitted at time {self.env.now}")
        self.jobs_queue.append(job)
        self.env.process(self.run_job(job))

    def run_job(self, job: Job):
        node = self.select_node_for_job(job)
        if node is None:
            logger.warning(f"No available node for job {job.job_id} at time {self.env.now}")
            return
        logger.info(f"Job {job.job_id} started on node {node.node_id} at time {self.env.now}")
        self.running_jobs[job.job_id] = node
        while not job.is_complete():
            yield self.env.timeout(1)  # Simulate 1 second time step
            job.run(1)
            node.update_temperature(job.average_power, 1)
        logger.info(f"Job {job.job_id} completed at time {self.env.now}")
        del self.running_jobs[job.job_id]

    def select_node_for_job(self, job: Job) -> Optional[Node]:
        # Simple selection: pick the node with the lowest current temperature
        if not self.nodes:
            return None
        selected_node = min(self.nodes, key=lambda n: n.current_temperature)
        return selected_node

    def get_user_resource_usage(self, user):
        # Placeholder for user resource usage calculation
        return 0

    def get_user_fair_share(self, user):
        # Placeholder for fair share calculation
        return 1

    def predict_energy_consumption(self, task, allocation):
        # Placeholder for energy consumption prediction
        return 1.0

    def get_renewable_energy_percentage(self, allocation):
        # Placeholder for renewable energy percentage
        return 50.0

    def get_node_temperatures(self):
        return {node.node_id: node.current_temperature for node in self.nodes}

    def predict_temperature_increase(self, task, allocation):
        # Placeholder for temperature increase prediction
        return {node.node_id: 5.0 for node in self.nodes}

    def get_available_resources(self):
        # Placeholder for available resources
        return self.nodes
