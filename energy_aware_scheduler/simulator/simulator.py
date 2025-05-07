import simpy
import logging
from typing import List, Optional
from .node import Node
from .job import Job
from .abc_optimizer import ArtificialBeeColony
import logging

logger = logging.getLogger(__name__)

class EnergyAwareSimulator:
    def __init__(self, env: simpy.Environment, nodes: List[Node]):
        self.env = env
        self.nodes = nodes
        self.jobs_queues: List[List[Job]] = []  # Multi-level queues
        self.running_jobs = {}
        self.abc_optimizer = None

    def initialize_queues(self, num_queues: int):
        self.jobs_queues = [[] for _ in range(num_queues)]

    def submit_job(self, job: Job, queue_index: int = 0):
        if queue_index >= len(self.jobs_queues):
            logger.warning(f"Queue index {queue_index} out of range, defaulting to 0")
            queue_index = 0
        job_id = getattr(job, 'job_id', None)
        if job_id is None:
            job_id = getattr(job, 'task_id', str(job))
        logger.info(f"Job {job_id} submitted to queue {queue_index} at time {self.env.now}")
        self.jobs_queues[queue_index].append(job)
        self.env.process(self.run_job(job))

    def run_job(self, job: Job):
        node = self.select_node_for_job(job)
        if node is None:
            job_id = getattr(job, 'job_id', None)
            if job_id is None:
                job_id = getattr(job, 'task_id', str(job))
            logger.warning(f"No available node for job {job_id} at time {self.env.now}")
            return
        job.assigned_node = node  # Assign node to job here
        job_id = getattr(job, 'job_id', None)
        if job_id is None:
            job_id = getattr(job, 'task_id', str(job))
        logger.info(f"Job {job_id} started on node {node.node_id} at time {self.env.now}")
        self.running_jobs[job_id] = node

        if hasattr(job, 'is_complete') and callable(getattr(job, 'is_complete')):
            while not job.is_complete():
                yield self.env.timeout(1)  # Simulate 1 second time step
                job.run(1)
                node.update_temperature(job.average_power, 1)
        else:
            # If no is_complete method, run for job.duration if available, else 1 step
            duration = getattr(job, 'duration', 1)
            for _ in range(int(duration)):
                yield self.env.timeout(1)
                power = getattr(job, 'average_power', 0)
                node.update_temperature(power, 1)

        logger.info(f"Job {job_id} completed at time {self.env.now}")
        del self.running_jobs[job_id]

    def select_node_for_job(self, job: Job) -> Optional[Node]:
        # Simple selection: pick the node with the lowest current temperature
        if not self.nodes:
            return None
        selected_node = min(self.nodes, key=lambda n: n.current_temperature)
        return selected_node

    def optimize_queues_with_abc(self):
        # Flatten jobs to solutions for ABC optimizer
        food_sources = []
        for queue in self.jobs_queues:
            for job in queue:
                food_sources.append({'completion_time': job.estimated_completion_time})

        if not food_sources:
            logger.info("No jobs to optimize in queues")
            return

        self.abc_optimizer = ArtificialBeeColony(food_sources)
        best_solution = self.abc_optimizer.optimize()
        logger.info(f"ABC optimization best solution: {best_solution}")

        # Reassign jobs to queues based on optimized completion times (simple example)
        # Here we just clear and reassign jobs to queues based on completion_time thresholds
        self.initialize_queues(len(self.jobs_queues))
        for job in sum(self.jobs_queues, []):
            if job.estimated_completion_time <= best_solution['completion_time']:
                self.jobs_queues[0].append(job)
            else:
                self.jobs_queues[-1].append(job)

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
