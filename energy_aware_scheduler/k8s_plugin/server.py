from flask import Flask, jsonify
from flask_cors import CORS
import threading
import simpy
import time
import logging
from simpy.core import EmptySchedule
from energy_aware_scheduler.hpc_extension.ml_scheduler import ReinforcementLearningScheduler
from energy_aware_scheduler.hpc_extension.scheduler_sjf_mmbf import SJFMmbfScheduler
from energy_aware_scheduler.hpc_extension.scheduler_sjf_elm import SJFEllmScheduler
from energy_aware_scheduler.hpc_extension.anfis_host_detection import ANFISHostDetection
from energy_aware_scheduler.hpc_extension.mmt_migration import MMTMigration
from energy_aware_scheduler.hpc_extension.ecc_encryption import ECCEncryption
from energy_aware_scheduler.simulator.simulator import EnergyAwareSimulator
from energy_aware_scheduler.simulator.node import Node
from energy_aware_scheduler.hpc_extension.hpc_task import HPCTask
from energy_aware_scheduler.telemetry.nvml_telemetry import AsyncNvmlTelemetry
from energy_aware_scheduler.telemetry.cpu_telemetry import CpuTelemetry

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize simpy environment and simulator
env = simpy.Environment()
# Define fan curves for nodes (example)
fan_curve = {
    30.0: 20.0,
    50.0: 50.0,
    70.0: 80.0,
    90.0: 100.0
}
nodes = [
    Node("node1", 64, 8, fan_curve=fan_curve),
    Node("node2", 64, 8, fan_curve=fan_curve)
]
simulator = EnergyAwareSimulator(env, nodes)
simulator.initialize_queues(1)  # Initialize one job queue

ml_scheduler = ReinforcementLearningScheduler(simulator)
sjf_mmbf_scheduler = SJFMmbfScheduler()
sjf_elm_scheduler = SJFEllmScheduler()
anfis_detector = ANFISHostDetection()
mmt_migrator = MMTMigration()
ecc_encryptor = ECCEncryption()

# Initialize NVML telemetry for real-time GPU data
nvml_telemetry = AsyncNvmlTelemetry()
nvml_telemetry.start()

# Initialize CPU telemetry for real-time CPU data
cpu_telemetry = CpuTelemetry()
cpu_telemetry.start()

def run_simulation():
    from energy_aware_scheduler.simulator.job import Job
    job1 = Job("job1", "workloadA", 50.0, 30)  # job_id, workload_type, average_power, duration
    job2 = Job("job2", "workloadB", 60.0, 45)
    simulator.submit_job(job1)
    simulator.submit_job(job2)
    logger.info("Submitted example jobs to simulator")

    while True:
        try:
            env.step()
            # Update fan speed for each node based on current temperature
            for node in nodes:
                node.fan_speed = node.get_fan_speed()
            logger.info(f"Simulation time: {env.now}, Running jobs: {len(simulator.running_jobs)}")
            time.sleep(0.1)  # Sleep to allow other threads to run and simulate time passing
        except EmptySchedule:
            logger.info("Simulation ended: no more scheduled events.")
            break

# Start simulation in a background thread
simulation_thread = threading.Thread(target=run_simulation, daemon=True)
simulation_thread.start()

@app.route('/api/scheduling_decisions')
def scheduling_decisions():
    import traceback
    tasks = [
        HPCTask("task1"),
        HPCTask("task2"),
    ]
    try:
        from flask import request
        scheduler_type = request.args.get('type', 'ml')
        if scheduler_type == 'ml':
            schedule = ml_scheduler.schedule(tasks, nodes)
        elif scheduler_type == 'sjf_mmbf':
            sjf_mmbf_scheduler.buffer_tasks(tasks)
            schedule = sjf_mmbf_scheduler.schedule(nodes)
        elif scheduler_type == 'sjf_elm':
            sjf_elm_scheduler.buffer_tasks(tasks)
            schedule = sjf_elm_scheduler.schedule(nodes)
        else:
            schedule = ml_scheduler.schedule(tasks, nodes)
    except Exception as e:
        traceback_str = traceback.format_exc()
        app.logger.error(f"Scheduling error traceback: {traceback_str}")
        return jsonify({"error": f"Scheduling error: {str(e)}"}), 500

    latest_gpu_data = nvml_telemetry.get_latest_data() or []
    latest_cpu_data = cpu_telemetry.get_latest_data() or {}

    response = []
    gpu_metrics = {}
    if isinstance(latest_gpu_data, list) and len(latest_gpu_data) > 0:
        gpu_metrics = latest_gpu_data[0] if isinstance(latest_gpu_data[0], dict) else {}

    for task_id, node in schedule.items():
        node_metrics = gpu_metrics
        gpu_power = node_metrics.get('power', 100.0)
        gpu_temp = node_metrics.get('temperature', node.current_temperature)
        cpu_percent = latest_cpu_data.get('cpu_percent', None)
        response.append({
            "taskId": task_id,
            "nodeId": node.node_id,
            "energy": gpu_power,
            "temperature": gpu_temp,
            "cpu_percent": cpu_percent,
        })
    return jsonify(response)

@app.route('/api/nodes')
def get_nodes():
    response = []
    for node in nodes:
        response.append({
            "node_id": node.node_id,
            "cpu_count": node.cpu_count,
            "gpu_count": node.gpu_count,
            "current_temperature": node.current_temperature,
            "fan_speed": node.fan_speed,
        })
    return jsonify(response)

@app.route('/api/tasks')
def get_tasks():
    running_count = len(simulator.running_jobs)
    queued_count = sum(len(queue) for queue in simulator.jobs_queues)
    app.logger.info(f"Running jobs count: {running_count}, Queued jobs count: {queued_count}")

    tasks = []
    for job_id, node in simulator.running_jobs.items():
        tasks.append({
            "taskId": job_id,
            "nodeId": node.node_id,
            "energy": 100.0,
            "temperature": node.current_temperature,
            "status": "running",
            "startTime": None,
            "endTime": None
        })
    for queue in simulator.jobs_queues:
        for job in queue:
            tasks.append({
                "taskId": job.job_id,
                "nodeId": None,
                "energy": 0.0,
                "temperature": None,
                "status": "queued",
                "startTime": None,
                "endTime": None
            })
    return jsonify(tasks)

@app.route('/api/telemetry')
def get_telemetry():
    gpu_data = nvml_telemetry.data_buffer
    cpu_data = cpu_telemetry.data_buffer
    combined_data = {
        "gpu": gpu_data,
        "cpu": cpu_data
    }
    return jsonify(combined_data)

@app.route('/healthz')
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
