import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';

function TelemetryCharts({ telemetryData }) {
  if (!telemetryData || telemetryData.length === 0) {
    return <div>No telemetry data available</div>;
  }

  let lastPower = 0;
  let lastTemperature = 0;
  let lastUtilization = 0;

  const sanitizedData = telemetryData.map(d => {
    const power = d.power != null ? d.power : lastPower;
    const temperature = d.temperature != null ? d.temperature : lastTemperature;
    const utilization = d.utilization != null ? d.utilization : lastUtilization;

    lastPower = power;
    lastTemperature = temperature;
    lastUtilization = utilization;

    return {
      timestamp: d.timestamp,
      power,
      temperature,
      utilization,
    };
  });

  return (
    <div>
      <h2>Telemetry Charts</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={sanitizedData}
          margin={{
            top: 5, right: 30, left: 20, bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="power" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="temperature" stroke="#82ca9d" />
          <Line type="monotone" dataKey="utilization" stroke="#ffc658" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TelemetryCharts;
