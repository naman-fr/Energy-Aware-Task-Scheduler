from typing import List, Dict
from energy_aware_scheduler.simulator.job import Job
from energy_aware_scheduler.simulator.node import Node
import logging

logger = logging.getLogger(__name__)

class SJFMmbfScheduler:
    def __init__(self):
        self.task_queues: Dict[int, List[Job]] = {}  # Multi-level queues keyed by task type

    def buffer_tasks(self, tasks: List[Job]):
        """
        Buffer tasks into queues based on their type or other criteria.
        """
        self.task_queues.clear()
        for task in tasks:
            task_type = getattr(task, 'task_type', 0)
            if task_type not in self.task_queues:
                self.task_queues[task_type] = []
            self.task_queues[task_type].append(task)
        # Sort each queue by shortest job first (completion time)
        for queue in self.task_queues.values():
            queue.sort(key=lambda t: t.estimated_completion_time)

    def schedule(self, nodes: List[Node]) -> Dict[str, Node]:
        """
        Schedule tasks to nodes using Min-Min Best Fit (MMBF) policy.
        Returns a mapping from task_id to Node.
        """
        schedule = {}
        available_nodes = nodes.copy()
        for task_type, queue in self.task_queues.items():
            for task in queue:
                if not available_nodes:
                    logger.warning("No available nodes to schedule tasks")
                    break
                # Select node with best fit (lowest temperature)
                best_node = min(available_nodes, key=lambda n: n.current_temperature)
                schedule[task.job_id] = best_node
                # Optionally update node state or remove from available_nodes if fully utilized
        return schedule
