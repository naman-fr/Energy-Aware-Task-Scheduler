import numpy as np
import random

class ReinforcementLearningScheduler:
    def __init__(self, system_model, learning_rate=0.01, discount_factor=0.9):
        self.system_model = system_model
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = {}  # state-action values

    def get_state(self, task, node):
        # Simplified state representation
        return (task.task_id, node.node_id)

    def choose_action(self, state, actions):
        # Epsilon-greedy policy
        epsilon = 0.1
        if random.random() < epsilon:
            return random.choice(actions)
        q_values = [self.q_table.get((state, a), 0) for a in actions]
        max_q = max(q_values)
        max_actions = [a for a, q in zip(actions, q_values) if q == max_q]
        return random.choice(max_actions)

    def update_q_value(self, state, action, reward, next_state, next_actions):
        current_q = self.q_table.get((state, action), 0)
        next_q_values = [self.q_table.get((next_state, a), 0) for a in next_actions]
        max_next_q = max(next_q_values) if next_q_values else 0
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def schedule(self, tasks, nodes):
        schedule = {}
        for task in tasks:
            state = None
            best_node = None
            best_q = float('-inf')
            for node in nodes:
                state = self.get_state(task, node)
                q_value = self.q_table.get((state, node.node_id), 0)
                if q_value > best_q:
                    best_q = q_value
                    best_node = node
            if best_node is None:
                best_node = random.choice(nodes)
            schedule[task.task_id] = best_node
        return schedule
