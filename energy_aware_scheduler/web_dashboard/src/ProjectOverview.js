import React from 'react';
import './ProjectOverview.css';

function ProjectOverview() {
  return (
    <div className="project-overview-container">
      <h2>Energy-Aware Task Scheduler Simulator and Dashboard</h2>
      <p>
        This project is a comprehensive energy-aware task scheduling system designed for high-performance computing (HPC) environments, especially targeting DGX GB200-style nodes. It integrates advanced scheduling algorithms, real-time telemetry, security features, and Kubernetes orchestration with a user-friendly web dashboard.
      </p>

      <h3>Core Features</h3>

      <section>
        <h4>1. Discrete-Event Simulator</h4>
        <ul>
          <li>Models HPC nodes with CPU and GPU counts, thermal parameters, and fan speeds.</li>
          <li>Simulates job workloads with detailed power and thermal dynamics.</li>
          <li>Uses SimPy for discrete-event simulation to realistically model job execution and resource usage.</li>
          <li>Supports multi-queue task management and Artificial Bee Colony (ABC) optimization for efficient task queuing.</li>
          <li>Modular, production-quality Python code with type hints and comprehensive logging.</li>
          <li>Unit tests ensure reliability and correctness of simulation components.</li>
        </ul>
      </section>

      <section>
        <h4>2. Advanced Scheduling Policies</h4>
        <ul>
          <li>Reinforcement Learning-based scheduler for adaptive task placement.</li>
          <li>Shortest Job First with Minimum Migration and Buffering Factor (SJF-MMBF).</li>
          <li>Shortest Job First with Extreme Learning Machine (SJF-ELM).</li>
          <li>Scheduling policies optimize energy consumption and performance.</li>
          <li>Collaborative scheduling integrates telemetry data for informed decisions.</li>
        </ul>
      </section>

      <section>
        <h4>3. Host Utilization and Migration</h4>
        <ul>
          <li>Over-utilized host detection using Adaptive Neuro-Fuzzy Inference System (ANFIS).</li>
          <li>Under-utilized host detection and VM migration using Minimum Migration Time (MMT) algorithm.</li>
          <li>Dynamic load balancing and energy reduction.</li>
        </ul>
      </section>

      <section>
        <h4>4. Cybersecurity and Intrusion Prevention</h4>
        <ul>
          <li>Elliptic Curve Cryptography (ECC) for secure communication and data protection.</li>
          <li>Key generation, shared key derivation, and AES-GCM encryption/decryption.</li>
          <li>Ensures secure task scheduling and telemetry data handling.</li>
        </ul>
      </section>

      <section>
        <h4>5. Real-Time Telemetry Integration</h4>
        <ul>
          <li>GPU telemetry using NVIDIA Management Library (NVML) for power, temperature, and clock speeds.</li>
          <li>CPU telemetry using psutil for utilization and frequency metrics.</li>
          <li>Asynchronous polling threads gather telemetry data continuously.</li>
          <li>Telemetry data exposed via REST APIs for real-time monitoring and dashboard visualization.</li>
        </ul>
      </section>

      <section>
        <h4>6. Kubernetes Scheduler Plugin</h4>
        <ul>
          <li>Custom Kubernetes scheduler plugin integrates energy-aware scheduling decisions.</li>
          <li>Collaborative scheduling and telemetry integration for optimized resource usage in containerized environments.</li>
          <li>Prometheus exporter and Helm charts for deployment and monitoring.</li>
        </ul>
      </section>

      <section>
        <h4>7. Web-Based Operational Dashboard</h4>
        <ul>
          <li>React-based frontend with real-time visualization of node status, task details, scheduling decisions, and telemetry charts.</li>
          <li>Responsive UI with charts powered by Recharts.</li>
          <li>Live data fetching from backend APIs with periodic polling for near real-time updates.</li>
        </ul>
      </section>

      <section>
        <h3>Scheduling Process Overview</h3>
        <p>
          The scheduling process in this project involves multiple integrated components working together to optimize task placement and resource utilization in HPC environments:
        </p>
        <ol>
          <li>
            <strong>Task Submission and Modeling:</strong> Jobs and tasks are submitted to the discrete-event simulator, which models their workload characteristics, power consumption, and duration.
          </li>
          <li>
            <strong>Telemetry Collection:</strong> Real-time telemetry data is collected asynchronously from GPUs (via NVML) and CPUs (via psutil), including power usage, temperature, clock speeds, and utilization metrics.
          </li>
          <li>
            <strong>Scheduling Decision Making:</strong> Multiple scheduling algorithms are available, including reinforcement learning-based schedulers, shortest job first variants (SJF-MMBF, SJF-ELM), and collaborative scheduling. These algorithms use telemetry data and workload models to make energy-efficient and performance-optimized scheduling decisions.
          </li>
          <li>
            <strong>Host Utilization and Migration:</strong> The system detects over-utilized and under-utilized hosts using ANFIS and other heuristics. VM migration is performed using the Minimum Migration Time (MMT) algorithm to balance load and reduce energy consumption.
          </li>
          <li>
            <strong>Security Integration:</strong> Elliptic Curve Cryptography (ECC) ensures secure communication and data protection during scheduling and telemetry data exchange.
          </li>
          <li>
            <strong>Kubernetes Integration:</strong> The custom Kubernetes scheduler plugin integrates these scheduling decisions into container orchestration, enabling energy-aware scheduling in Kubernetes clusters.
          </li>
          <li>
            <strong>Visualization and Monitoring:</strong> The React-based web dashboard visualizes node status, task details, scheduling decisions, and telemetry charts in real-time, providing operators with actionable insights.
          </li>
        </ol>
        <p>
          This integrated approach enables dynamic, secure, and energy-efficient task scheduling tailored for HPC environments.
        </p>
      </section>

      <section>
        <h3>Scheduling Process Visualization</h3>
        <p>
          The scheduling process can be understood as a flow of inputs, processing, and outputs, integrating all major components and algorithms in the project:
        </p>
        <ul>
          <li><strong>Input:</strong> User submits jobs/tasks with workload characteristics and requirements.</li>
          <li><strong>Telemetry Data:</strong> Continuous real-time collection of GPU and CPU metrics, including power, temperature, utilization, and fan speeds.</li>
          <li><strong>Processing:</strong> The scheduler uses telemetry data and workload models to run advanced scheduling algorithms (Reinforcement Learning, SJF-MMBF, SJF-ELM, Collaborative Scheduling).</li>
          <li><strong>Host Analysis:</strong> ANFIS detects over-utilized hosts; MMT algorithm manages VM migrations to balance load and optimize energy.</li>
          <li><strong>Security:</strong> ECC encryption secures communication and data exchange during scheduling and telemetry handling.</li>
          <li><strong>Integration:</strong> Kubernetes scheduler plugin applies scheduling decisions to container orchestration.</li>
          <li><strong>Output:</strong> Tasks are assigned to nodes dynamically, optimizing for energy efficiency and performance.</li>
          <li><strong>Visualization:</strong> Web dashboard displays real-time node status, task assignments, scheduling decisions, and telemetry charts for monitoring and management.</li>
        </ul>
        <p>
          This comprehensive flow ensures that tasks are scheduled intelligently based on real-time system state, advanced algorithms, and secure communication, providing an effective energy-aware HPC scheduling solution.
        </p>
      </section>

      <section>
        <h4>8. Deployment and CI/CD</h4>
        <ul>
          <li>Dockerfile and Helm chart for containerized deployment on Kubernetes clusters.</li>
          <li>GitHub Actions configured for continuous integration and deployment.</li>
          <li>Grafana dashboards included for enhanced monitoring and visualization.</li>
        </ul>
      </section>
    </div>
  );
}

export default ProjectOverview;
