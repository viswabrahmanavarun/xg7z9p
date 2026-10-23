// src/components/Dashboard.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DataPoint {
  startTime: string; // ISO string
  generation: number;
}

interface DashboardProps {
  forecast: DataPoint[];
  actual: DataPoint[];
}

// Merge forecast and actual series by timestamp for charting
const mergeSeries = (forecast: DataPoint[], actual: DataPoint[]) => {
  const map = new Map<string, { forecast?: number; actual?: number }>();
  forecast.forEach((p) => {
    const key = new Date(p.startTime).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    if (!map.has(key)) map.set(key, {});
    map.get(key)!.forecast = p.generation;
  });
  actual.forEach((p) => {
    const key = new Date(p.startTime).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    if (!map.has(key)) map.set(key, {});
    map.get(key)!.actual = p.generation;
  });
  // Convert to array sorted by time
  const data = Array.from(map.entries())
    .map(([time, vals]) => ({ time, ...vals }))
    .sort((a, b) => a.time.localeCompare(b.time));
  return data;
};

const Dashboard: React.FC<DashboardProps> = ({ forecast, actual }) => {
  const data = mergeSeries(forecast, actual);
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="forecast" stroke="#8884d8" name="Forecast (MW)" dot={false} />
        <Line type="monotone" dataKey="actual" stroke="#82ca9d" name="Actual (MW)" dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default Dashboard;
