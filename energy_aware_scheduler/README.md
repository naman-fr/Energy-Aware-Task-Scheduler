# Energy-Aware Task Scheduler Simulator

This project is a discrete-event simulator modeling power, thermal, and job dynamics on DGX GB200-style nodes using SimPy. It serves as the foundation for an energy-aware Kubernetes scheduler plugin.

## Features

- SimPy-based event-driven simulation
- Node modeling with CPU/GPU counts and thermal parameters
- Job modeling with workload characteristics
- Thermal dynamics simulation with discrete temperature updates
- Modular, production-quality Python code with type hints and logging
- Unit tests for core components

## Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests:

```bash
pytest
```

## Project Structure

- `simulator/` - Core simulator modules
- `tests/` - Unit tests
- `README.md` - Project overview
- `requirements.txt` - Python dependencies

## Next Steps

- Extend simulator with real workload profiles
- Integrate with NVML for real-time telemetry
- Develop Kubernetes scheduler plugin
