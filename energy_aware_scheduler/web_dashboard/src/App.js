import React, { useEffect, useState } from 'react';
import NodeStatus from './NodeStatus';
import TaskDetails from './TaskDetails';
import TelemetryCharts from './TelemetryCharts';
import ProjectOverview from './ProjectOverview';
import './App.css';

function App() {
  const [scheduleData, setScheduleData] = useState([]);
  const [nodes, setNodes] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [telemetryData, setTelemetryData] = useState([]);
  const [error, setError] = useState(null);
  const [selectedTab, setSelectedTab] = useState('overview');

  const POLL_INTERVAL = 5000;

  useEffect(() => {
    let isMounted = true;

    const fetchScheduling = () => {
      fetch('/api/scheduling_decisions')
        .then((response) => {
          if (!response.ok) throw new Error('Network response was not ok');
          return response.json();
        })
        .then((data) => {
          console.log('Scheduling data:', data);
          if (isMounted) setScheduleData(data);
        })
        .catch((error) => {
          console.error('Error fetching scheduling:', error);
          if (isMounted) setError(error.message);
        });
    };

    fetchScheduling();
    const intervalId = setInterval(fetchScheduling, POLL_INTERVAL);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    let isMounted = true;

    const fetchNodes = () => {
      fetch('/api/nodes')
        .then((response) => {
          if (!response.ok) throw new Error('Network response was not ok');
          return response.json();
        })
        .then((data) => {
          console.log('Nodes data:', data);
          if (isMounted) setNodes(data);
        })
        .catch((error) => {
          console.error('Error fetching nodes:', error);
          if (isMounted) setError(error.message);
        });
    };

    fetchNodes();
    const intervalId = setInterval(fetchNodes, POLL_INTERVAL);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    let isMounted = true;

    const fetchTasks = () => {
      fetch('/api/tasks')
        .then((response) => {
          if (!response.ok) throw new Error('Network response was not ok');
          return response.json();
        })
        .then((data) => {
          console.log('Tasks data:', data);
          if (isMounted) setTasks(data);
        })
        .catch((error) => {
          console.error('Error fetching tasks:', error);
          if (isMounted) setError(error.message);
        });
    };

    fetchTasks();
    const intervalId = setInterval(fetchTasks, POLL_INTERVAL);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    let isMounted = true;

    const fetchTelemetry = () => {
      fetch('/api/telemetry')
        .then((response) => {
          if (!response.ok) throw new Error('Network response was not ok');
          return response.json();
        })
        .then((data) => {
          console.log('Telemetry data:', data);
          if (!isMounted) return;
          const mergedData = [];
          const gpuData = data.gpu || [];
          const cpuData = data.cpu || [];
          const maxLength = Math.max(gpuData.length, cpuData.length);
          for (let i = 0; i < maxLength; i++) {
            // gpuData[i] is an array of GPU metrics objects for that timestamp
            let avgPower = null;
            let avgTemp = null;
            if (gpuData[i] && gpuData[i].length > 0) {
              const powerValues = gpuData[i].map(gpu => gpu.power).filter(p => p != null);
              const tempValues = gpuData[i].map(gpu => gpu.temperature).filter(t => t != null);
              avgPower = powerValues.length > 0 ? powerValues.reduce((a,b) => a + b, 0) / powerValues.length : null;
              avgTemp = tempValues.length > 0 ? tempValues.reduce((a,b) => a + b, 0) / tempValues.length : null;
            }
            mergedData.push({
              timestamp: (gpuData[i]?.[0]?.timestamp || cpuData[i]?.timestamp) || null,
              power: avgPower,
              temperature: avgTemp,
              utilization: cpuData[i]?.cpu_percent || null,
            });
          }
          setTelemetryData(mergedData);
        })
        .catch((error) => {
          console.error('Error fetching telemetry:', error);
          if (isMounted) setError(error.message);
        });
    };

    fetchTelemetry();
    const intervalId = setInterval(fetchTelemetry, POLL_INTERVAL);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  if (error) {
    return <div className="error">Error fetching data: {error}</div>;
  }

  console.log('Data lengths:', {
    scheduleDataLength: scheduleData.length,
    nodesLength: nodes.length,
    tasksLength: tasks.length,
    telemetryDataLength: telemetryData.length,
  });

  if (
    (selectedTab !== 'overview') &&
    (scheduleData.length === 0 && nodes.length === 0 && tasks.length === 0 && telemetryData.length === 0)
  ) {
    return <div className="loading">Loading data...</div>;
  }

  return (
    <div className="app-container">
      <h1>Energy-Aware Scheduler Dashboard</h1>
      <nav className="nav-tabs">
        <button className={selectedTab === 'overview' ? 'active' : ''} onClick={() => setSelectedTab('overview')}>Project Overview</button>
        <button className={selectedTab === 'scheduling' ? 'active' : ''} onClick={() => setSelectedTab('scheduling')}>Scheduling Decisions</button>
        <button className={selectedTab === 'nodes' ? 'active' : ''} onClick={() => setSelectedTab('nodes')}>Node Status</button>
        <button className={selectedTab === 'tasks' ? 'active' : ''} onClick={() => setSelectedTab('tasks')}>Task Details</button>
        <button className={selectedTab === 'telemetry' ? 'active' : ''} onClick={() => setSelectedTab('telemetry')}>Telemetry Charts</button>
      </nav>
      <div className="tab-content">
        {selectedTab === 'overview' && <ProjectOverview />}
        {selectedTab === 'scheduling' && (
          <ul>
            {scheduleData && scheduleData.map((item) => (
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
