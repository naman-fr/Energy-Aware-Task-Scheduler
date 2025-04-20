import unittest
import json
from energy_aware_scheduler.k8s_plugin.plugin import EnergyAwareSchedulerPlugin
from energy_aware_scheduler.k8s_plugin.server import app

class TestEnergyAwareSchedulerPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = EnergyAwareSchedulerPlugin()
        self.client = app.test_client()

    def test_filter_method(self):
        node_info = {'power': 200, 'temperature': 70}
        self.assertTrue(self.plugin.filter(node_info))
        node_info = {'power': 300, 'temperature': 70}
        self.assertFalse(self.plugin.filter(node_info))
        node_info = {'power': 200, 'temperature': 90}
        self.assertFalse(self.plugin.filter(node_info))

    def test_score_method(self):
        node_info = {'power': 100, 'temperature': 50}
        score = self.plugin.score(node_info)
        expected_score = 0.7 * 100 + 0.3 * 50
        self.assertAlmostEqual(score, expected_score)

    def test_filter_endpoint(self):
        response = self.client.post('/filter', json={'node_info': {'power': 200, 'temperature': 70}})
        data = json.loads(response.data)
        self.assertTrue(data['allowed'])
        response = self.client.post('/filter', json={'node_info': {'power': 300, 'temperature': 70}})
        data = json.loads(response.data)
        self.assertFalse(data['allowed'])

    def test_score_endpoint(self):
        response = self.client.post('/score', json={'node_info': {'power': 100, 'temperature': 50}})
        data = json.loads(response.data)
        expected_score = 0.7 * 100 + 0.3 * 50
        self.assertAlmostEqual(data['score'], expected_score)

if __name__ == '__main__':
    unittest.main()
