import React from 'react';

function TaskDetails({ tasks }) {
  return (
    <div>
      <h2>Task Details</h2>
      <table>
        <thead>
          <tr>
            <th>Task ID</th>
            <th>Node ID</th>
            <th>Energy (W)</th>
            <th>Temperature (°C)</th>
            <th>Status</th>
            <th>Start Time</th>
            <th>End Time</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.taskId}>
              <td>{task.taskId}</td>
              <td>{task.nodeId}</td>
              <td>{task.energy}</td>
              <td>{task.temperature}</td>
              <td>{task.status}</td>
              <td>{task.startTime}</td>
              <td>{task.endTime}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TaskDetails;
