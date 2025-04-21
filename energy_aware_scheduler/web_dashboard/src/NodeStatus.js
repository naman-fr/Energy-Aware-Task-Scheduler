import React from 'react';

function NodeStatus({ nodes }) {
  return (
    <div>
      <h2>Node Status</h2>
      <table>
        <thead>
          <tr>
            <th>Node ID</th>
            <th>CPU Count</th>
            <th>GPU Count</th>
            <th>Current Temperature (°C)</th>
            <th>Fan Speed (%)</th>
          </tr>
        </thead>
        <tbody>
          {nodes.map((node) => (
            <tr key={node.node_id}>
              <td>{node.node_id}</td>
              <td>{node.cpu_count}</td>
              <td>{node.gpu_count}</td>
              <td>{node.current_temperature.toFixed(1)}</td>
              <td>{node.fan_speed.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default NodeStatus;
