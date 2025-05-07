from typing import List, Dict
from energy_aware_scheduler.simulator.job import Job
from energy_aware_scheduler.simulator.node import Node
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SJFEllmScheduler:
    def __init__(self):
        self.task_queues: Dict[int, List[Job]] = {}  # Multi-level queues keyed by task type
        self.alpha = 0.5  # Weight parameter for time-averaged completion time
        self.expected_completion_time = 0.0

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

    def elm_predict(self, features: np.ndarray) -> float:
        """
        Placeholder for Extreme Learning Machine prediction.
        In real implementation, this would use a trained ELM model.
        """
        # For demonstration, return a random value
        return np.random.rand()

    def schedule(self, nodes: List[Node]) -> Dict[str, Node]:
        """
        Schedule tasks to nodes using ELM-based policy.
        Returns a mapping from task_id to Node.
        """
        schedule = {}
        available_nodes = nodes.copy()
        for task_type, queue in self.task_queues.items():
            for task in queue:
                if not available_nodes:
                    logger.warning("No available nodes to schedule tasks")
                    break
                # Extract features for ELM prediction (example: task length, node temperature)
                features = np.array([task.estimated_completion_time])
                # Predict scheduling score for each node
                node_scores = []
                for node in available_nodes:
                    node_feature = np.array([node.current_temperature])
                    combined_features = np.concatenate((features, node_feature))
                    score = self.elm_predict(combined_features)
                    node_scores.append((node, score))
                # Select node with highest score
                best_node = max(node_scores, key=lambda x: x[1])[0]
                schedule[task.job_id] = best_node
                # Optionally update node state or remove from available_nodes if fully utilized
        return schedule
