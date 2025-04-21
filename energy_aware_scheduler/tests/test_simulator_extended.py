import pytest
import simpy
from energy_aware_scheduler.simulator.simulator import EnergyAwareSimulator
from energy_aware_scheduler.simulator.node import Node
from energy_aware_scheduler.simulator.job import Job

def test_simulator_basic_job_execution():
    env = simpy.Environment()
    nodes = [Node("node1", cpu_count=16, gpu_count=4, thermal_capacity=100.0)]
    simulator = EnergyAwareSimulator(env, nodes)

    job = Job("job1", "test_workload", average_power=100, duration=5)
    simulator.add_job(job)

    simulator.run(until=10)

    assert job.is_complete()
    assert job.assigned_node == nodes[0]
    assert nodes[0].current_temperature >= 25.0  # Temperature should have increased

def test_multiple_jobs_execution():
    env = simpy.Environment()
    nodes = [Node("node1", cpu_count=16, gpu_count=4, thermal_capacity=100.0)]
    simulator = EnergyAwareSimulator(env, nodes)

    job1 = Job("job1", "workload1", average_power=100, duration=3)
    job2 = Job("job2", "workload2", average_power=150, duration=4)
    simulator.add_job(job1)
    simulator.add_job(job2)

    simulator.run(until=10)

    assert job1.is_complete()
    assert job2.is_complete()
    assert job1.assigned_node == nodes[0]
    assert job2.assigned_node == nodes[0]
