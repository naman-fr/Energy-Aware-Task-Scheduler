import unittest
from unittest.mock import MagicMock
from kubernetes.client.models import V1Pod
from energy_aware_scheduler.k8s_plugin.plugin import EnergyAwareSchedulerPlugin

class TestEnergyAwareSchedulerPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = EnergyAwareSchedulerPlugin()
        self.mock_pod = MagicMock(spec=V1Pod)
        self.mock_pod.metadata.name = "test-pod"
        self.mock_node = MagicMock()
        self.mock_node.node_id = "node-1"
        self.mock_node.index = 0

    def test_filter(self):
        nodes = [self.mock_node]
        suitable_nodes = self.plugin.filter(self.mock_pod, nodes)
        self.assertIn(self.mock_node, suitable_nodes)

    def test_score(self):
        nodes = [self.mock_node]
        scores = self.plugin.score(self.mock_pod, nodes)
        self.assertIn(self.mock_node.node_id, scores)
        self.assertIsInstance(scores[self.mock_node.node_id], (int, float))

    def test_reserve_and_permit(self):
        self.plugin.reserve(self.mock_pod, self.mock_node)
        self.plugin.permit(self.mock_pod, self.mock_node)

    def test_preempt(self):
        nodes = [self.mock_node]
        preempted = self.plugin.preempt(self.mock_pod, nodes)
        self.assertIsInstance(preempted, list)

    def test_gang_schedule(self):
        pods = [self.mock_pod]
        result = self.plugin.gang_schedule(pods)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
