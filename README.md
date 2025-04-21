# Energy-Aware Task Scheduler Simulator and Dashboard

This project is a comprehensive energy-aware task scheduling system designed for high-performance computing (HPC) environments, particularly targeting DGX GB200-style nodes. It combines a discrete-event simulator, real-time telemetry integration, and a Kubernetes scheduler plugin with a web-based operational dashboard.

## Features

### Simulator
- **Discrete-event simulation** using SimPy to model power, thermal, and job dynamics on HPC nodes.
- **Node modeling** with CPU and GPU counts, thermal parameters, and fan speed.
- **Job modeling** with workload characteristics and scheduling.
- **Thermal dynamics simulation** with discrete temperature updates.
- **Modular, production-quality Python code** with type hints and logging.
- **Unit tests** covering core components to ensure reliability.

### Real-Time Telemetry
- **GPU telemetry** using NVIDIA Management Library (NVML) via `pynvml` for power, temperature, and clock speed.
- **CPU telemetry** using `psutil` for CPU utilization and frequency.
- Asynchronous telemetry collection with background polling threads.
- Telemetry data exposed via REST API endpoints for integration with dashboards.

### Kubernetes Scheduler Plugin
- Energy-aware scheduling decisions integrated into Kubernetes via a custom scheduler plugin.
- Collaborative scheduling and telemetry integration for optimized resource usage.

### Web Dashboard
- React-based frontend providing real-time visualization of:
  - Node status (CPU/GPU counts, temperatures, fan speeds).
  - Task details and scheduling decisions.
  - Telemetry charts for power, temperature, and utilization over time.
- Integration with backend APIs to fetch live telemetry and scheduling data.
- Responsive UI with charts powered by Recharts.

### Deployment
- Dockerfile and Helm chart for containerized deployment on Kubernetes clusters.
- Prometheus exporter for metrics collection and monitoring.
- CI/CD pipeline configured via GitHub Actions.

## Project Structure

- `simulator/` - Core simulation modules modeling nodes, jobs, and thermal dynamics.
- `hpc_extension/` - HPC-specific scheduling algorithms, ML schedulers, and integration adapters.
- `telemetry/` - NVML and CPU telemetry collectors with asynchronous polling.
- `k8s_plugin/` - Kubernetes scheduler plugin, telemetry integration, and REST API server.
- `web_dashboard/` - React frontend source code and static assets.
- `tests/` - Unit and integration tests for simulator and telemetry components.
- `helm/` - Helm chart templates for Kubernetes deployment.
- `grafana/` - Grafana dashboard JSON for monitoring visualization.
- `Dockerfile` - Container image build configuration.
- `.github/workflows/` - CI/CD pipeline definitions.

## Setup and Usage

### Prerequisites
- Python 3.8+
- Node.js and npm
- Docker and Kubernetes cluster (for deployment)

### Backend Setup
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python -m energy_aware_scheduler.k8s_plugin.server
   ```

### Frontend Setup
1. Navigate to the web dashboard directory:
   ```bash
   cd energy_aware_scheduler/web_dashboard
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Access the dashboard at `http://localhost:3000`.

### Deployment
- Build and deploy using the provided Dockerfile and Helm chart for Kubernetes environments.
- Use Prometheus and Grafana for monitoring and visualization.

## Testing
- Run unit tests with:
  ```bash
  pytest
  ```

## Next Steps and Enhancements
- Extend simulator with real workload profiles and fault tolerance.
- Enhance ML scheduler with advanced reinforcement learning models.
- Improve telemetry integration with historical data storage and analysis.
- Expand dashboard with additional metrics and alerting capabilities.
- Optimize Kubernetes scheduler plugin for multi-cluster and cloud bursting scenarios.

## Contributing
Contributions are welcome! Please submit issues and pull requests via GitHub.

## License
This project is licensed under the MIT License.
