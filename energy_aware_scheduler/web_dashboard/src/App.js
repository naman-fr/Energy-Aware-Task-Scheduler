import React, { useEffect, useState } from 'react';
import NodeStatus from './NodeStatus';
import TaskDetails from './TaskDetails';
import TelemetryCharts from './TelemetryCharts';

function App() {
  const [scheduleData, setScheduleData] = useState(null);
  const [nodes, setNodes] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [telemetryData, setTelemetryData] = useState([]);
  const [error, setError] = useState(null);
  const [selectedTab, setSelectedTab] = useState('scheduling');

  useEffect(() => {
    fetch('http://localhost:5000/api/scheduling_decisions')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setScheduleData(data))
      .catch((error) => setError(error.message));
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/api/nodes')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setNodes(data))
      .catch((error) => setError(error.message));
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/api/tasks')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setTasks(data))
      .catch((error) => setError(error.message));
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/api/telemetry')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setTelemetryData(data))
      .catch((error) => setError(error.message));
  }, []);

  if (error) {
    return <div>Error fetching data: {error}</div>;
  }

  if (
    !scheduleData ||
    nodes.length === 0 ||
    tasks.length === 0 ||
    telemetryData.length === 0
  ) {
    return <div>Loading data...</div>;
  }

  return (
    <div>
      <h1>Energy-Aware Scheduler Dashboard</h1>
      <nav>
        <button onClick={() => setSelectedTab('scheduling')}>Scheduling Decisions</button>
        <button onClick={() => setSelectedTab('nodes')}>Node Status</button>
        <button onClick={() => setSelectedTab('tasks')}>Task Details</button>
        <button onClick={() => setSelectedTab('telemetry')}>Telemetry Charts</button>
      </nav>
      <div>
        {selectedTab === 'scheduling' && (
          <ul>
            {scheduleData.map((item) => (
              <li key={item.taskId}>
                Task {item.taskId} assigned to Node {item.nodeId} - Energy: {item.energy}W, Temp: {item.temperature}°C
              </li>
            ))}
          </ul>
        )}
        {selectedTab === 'nodes' && <NodeStatus nodes={nodes} />}
        {selectedTab === 'tasks' && <TaskDetails tasks={tasks} />}
        {selectedTab === 'telemetry' && <TelemetryCharts telemetryData={telemetryData} />}
      </div>
    </div>
  );
}

export default App;
