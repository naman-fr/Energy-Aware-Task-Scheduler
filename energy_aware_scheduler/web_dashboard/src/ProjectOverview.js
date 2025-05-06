import React from 'react';

function ProjectOverview() {
  return (
    <div>
      <h2>Energy-Aware Task Scheduler Project Overview</h2>
      <p>
        This project is designed to help manage and schedule computing tasks in large, powerful computer systems called High-Performance Computing (HPC) environments.
        The goal is to save energy and keep the system running efficiently and safely.
      </p>
      <h3>What the Project Does</h3>
      <ul>
        <li><strong>Simulation:</strong> It creates a virtual model of the computer system to test how tasks use power and generate heat.</li>
        <li><strong>Telemetry:</strong> It collects real-time data about the system's power use, temperature, and performance.</li>
        <li><strong>Scheduling:</strong> It decides the best way to assign tasks to different parts of the system to save energy and avoid overheating.</li>
        <li><strong>Kubernetes Integration:</strong> It works with Kubernetes, a system that manages many computer tasks, to apply energy-saving scheduling in real environments.</li>
        <li><strong>Web Dashboard:</strong> It provides an easy-to-use website where you can see what's happening in the system, including task assignments, node status, and energy use.</li>
      </ul>
      <h3>How It Works Together</h3>
      <p>
        1. The <em>Simulator</em> models the computer system and how tasks affect power and temperature.<br/>
        2. The <em>Telemetry</em> system collects live data from the real hardware.<br/>
        3. The <em>Scheduler</em> uses this information to decide where to run tasks to save energy and keep the system cool.<br/>
        4. The <em>Kubernetes Plugin</em> applies these decisions in real computing environments.<br/>
        5. The <em>Web Dashboard</em> shows all this information in a clear, visual way so users can monitor the system easily.
      </p>
      <h3>Using the Dashboard</h3>
      <p>
        Use the tabs to explore different parts of the system:<br/>
        - <strong>Project Overview:</strong> This guide.<br/>
        - <strong>Scheduling Decisions:</strong> See which tasks are running where and their energy use.<br/>
        - <strong>Node Status:</strong> Check the health and temperature of each computer node.<br/>
        - <strong>Task Details:</strong> View detailed information about each task.<br/>
        - <strong>Telemetry Charts:</strong> Watch live graphs of power, temperature, and performance metrics.
      </p>
      <p>
        This project helps make powerful computing systems more energy-efficient and reliable, saving costs and protecting hardware.
      </p>
    </div>
  );
}

export default ProjectOverview;
