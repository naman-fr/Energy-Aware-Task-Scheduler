import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import simpy
from energy_aware_scheduler.simulator.node import Node
from energy_aware_scheduler.simulator.job import Job
from energy_aware_scheduler.simulator.simulator import EnergyAwareSimulator
from energy_aware_scheduler.hpc_extension.hpc_task import HPCTask

def test_node_temperature_update():
    node = Node("node1", cpu_count=8, gpu_count=4, nvidia_ai_chip_count=0, thermal_capacity=100.0)
    initial_temp = node.current_temperature
    node.update_temperature(power_draw=50.0, time_interval=2.0)
    assert node.current_temperature > initial_temp

def test_job_run_and_completion():
    job = Job("job1", workload_type="BERT", average_power=100.0, duration=5.0)
    assert not job.is_complete()
    job.run(3.0)
    assert job.remaining_time == 2.0
    job.run(2.0)
    assert job.is_complete()

def test_simulator_job_submission_and_run():
    env = simpy.Environment()
    node = Node("node1", cpu_count=8, gpu_count=4, nvidia_ai_chip_count=0, thermal_capacity=100.0)
    simulator = EnergyAwareSimulator(env, [node])
    simulator.initialize_queues(1)
    job = Job("job1", workload_type="ResNet", average_power=80.0, duration=3.0)
    simulator.submit_job(job)
    env.run()
    assert job.is_complete()
    assert node.current_temperature > 25.0

def test_hpc_task_run():
    env = simpy.Environment()
    node1 = Node("node1", cpu_count=16, gpu_count=2, nvidia_ai_chip_count=1, thermal_capacity=100.0)
    node2 = Node("node2", cpu_count=16, gpu_count=2, nvidia_ai_chip_count=1, thermal_capacity=100.0)
    nodes = [node1, node2]
    sim = EnergyAwareSimulator(env, nodes)  # Removed system_topology argument

    hpc_task = HPCTask("hpc_job1")
    hpc_task.set_computation_profile({"required_nodes": 2, "cpus": 16, "gpus": 2, "nvidia_ai_chips": 1})
    hpc_task.set_communication_pattern({"type": "nearest_neighbor"})

    sim.initialize_queues(1)
    sim.submit_job(hpc_task)
    env.run()
    assert hpc_task.is_complete()
