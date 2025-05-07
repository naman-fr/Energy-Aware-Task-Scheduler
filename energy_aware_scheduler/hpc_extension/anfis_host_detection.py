import numpy as np
import logging

logger = logging.getLogger(__name__)

class ANFISHostDetection:
    def __init__(self):
        # Initialize ANFIS parameters (premise and consequent)
        self.a = 1.0
        self.b = 2.0
        self.c = 0.5
        self.p = 0.1
        self.q = 0.1
        self.r = 0.0

    def bell_membership(self, x, a, b, c):
        return 1.0 / (1.0 + ((x - c) / a) ** (2 * b))

    def compute_rule_strengths(self, cpu_util, mem_util):
        w1 = self.bell_membership(cpu_util, self.a, self.b, self.c) * self.bell_membership(mem_util, self.a, self.b, self.c)
        w2 = (1 - self.bell_membership(cpu_util, self.a, self.b, self.c)) * (1 - self.bell_membership(mem_util, self.a, self.b, self.c))
        return w1, w2

    def normalize_strengths(self, w1, w2):
        total = w1 + w2
        if total == 0:
            return 0, 0
        return w1 / total, w2 / total

    def predict_over_utilization(self, cpu_util, mem_util):
        w1, w2 = self.compute_rule_strengths(cpu_util, mem_util)
        w1_norm, w2_norm = self.normalize_strengths(w1, w2)
        f1 = self.p * cpu_util + self.q * mem_util + self.r
        f2 = self.p * (1 - cpu_util) + self.q * (1 - mem_util) + self.r
        output = w1_norm * f1 + w2_norm * f2
        logger.debug(f"ANFIS prediction: cpu_util={cpu_util}, mem_util={mem_util}, output={output}")
        return output

    def detect_over_utilized_hosts(self, hosts_metrics):
        """
        hosts_metrics: list of dicts with 'cpu_util' and 'mem_util' keys
        Returns list of host indices that are over-utilized
        """
        over_utilized = []
        for idx, metrics in enumerate(hosts_metrics):
            cpu_util = metrics.get('cpu_util', 0)
            mem_util = metrics.get('mem_util', 0)
            score = self.predict_over_utilization(cpu_util, mem_util)
            if score > 0.7:  # Threshold for over-utilization
                over_utilized.append(idx)
        return over_utilized
