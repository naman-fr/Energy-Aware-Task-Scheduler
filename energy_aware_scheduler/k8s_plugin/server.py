from flask import Flask, jsonify
from flask_cors import CORS
from energy_aware_scheduler.hpc_extension.ml_scheduler import ReinforcementLearningScheduler
from energy_aware_scheduler.simulator.simulator import EnergyAwareSimulator
from energy_aware_scheduler.simulator.node import Node
from energy_aware_scheduler.hpc_extension.hpc_task import HPCTask
from energy_aware_scheduler.telemetry.nvml_telemetry import AsyncNvmlTelemetry
from energy_aware_scheduler.telemetry.cpu_telemetry import CpuTelemetry

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize simulator and ML scheduler (placeholders)
env = None  # Should be simpy.Environment() in real setup
nodes = [Node("node1", 64, 8), Node("node2", 64, 8)]
simulator = EnergyAwareSimulator(env, nodes)
ml_scheduler = ReinforcementLearningScheduler(simulator)

# Initialize NVML telemetry for real-time GPU data
nvml_telemetry = AsyncNvmlTelemetry()
nvml_telemetry.start()

# Initialize CPU telemetry for real-time CPU data
cpu_telemetry = CpuTelemetry()
cpu_telemetry.start()

@app.route('/api/scheduling_decisions')
def scheduling_decisions():
    import traceback
    # Placeholder tasks
    tasks = [
        HPCTask("task1"),
        HPCTask("task2"),
    ]
    try:
        schedule = ml_scheduler.schedule(tasks, nodes)
    except Exception as e:
        traceback_str = traceback.format_exc()
        app.logger.error(f"Scheduling error traceback: {traceback_str}")
        return jsonify({"error": f"Scheduling error: {str(e)}"}), 500

    latest_gpu_data = nvml_telemetry.get_latest_data() or []
    latest_cpu_data = cpu_telemetry.get_latest_data() or {}

    response = []
    # latest_gpu_data is a list of dicts for each GPU device, no node_id key
    # We cannot key by node_id, so fallback to first GPU metrics for all nodes
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
            "fan_speed": getattr(node, 'fan_speed', 50.0),  # placeholder if attribute missing
        })
    return jsonify(response)

@app.route('/api/tasks')
def get_tasks():
    # Placeholder tasks with additional details
    tasks = [
        {
            "taskId": "task1",
            "nodeId": "node1",
            "energy": 120.5,
            "temperature": 70.2,
            "status": "running",
            "startTime": "2024-06-01T10:00:00Z",
            "endTime": "2024-06-01T12:00:00Z"
        },
        {
            "taskId": "task2",
            "nodeId": "node2",
            "energy": 110.0,
            "temperature": 68.5,
            "status": "queued",
            "startTime": "2024-06-01T11:00:00Z",
            "endTime": "2024-06-01T13:00:00Z"
        }
    ]
    return jsonify(tasks)

@app.route('/api/telemetry')
def get_telemetry():
    # Return the latest telemetry data buffer including CPU and GPU data
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
