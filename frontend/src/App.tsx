import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import MetricsTable from './components/MetricsTable';
import { useQuery } from 'react-query';
import { fetchForecasts, fetchActuals, fetchMetrics } from './api';
import './index.css';

const App: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>(() => {
    const today = new Date();
    // default to a date in January 2026 (e.g., 2026-01-01)
    return '2026-01-01';
  });

  const { data: forecastData, isLoading: loadingForecast } = useQuery(
    ['forecast', selectedDate],
    () => fetchForecasts(selectedDate),
    { staleTime: 5 * 60 * 1000 }
  );
  const { data: actualData, isLoading: loadingActual } = useQuery(
    ['actual', selectedDate],
    () => fetchActuals(selectedDate),
    { staleTime: 5 * 60 * 1000 }
  );
  const { data: metricsData, isLoading: loadingMetrics } = useQuery(
    ['metrics', selectedDate],
    () => fetchMetrics(selectedDate),
    { staleTime: 5 * 60 * 1000 }
  );

  const loading = loadingForecast || loadingActual || loadingMetrics;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Renewable Wind Forecast Dashboard</h1>
      <div className="mb-4">
        <label className="mr-2 font-medium" htmlFor="datePicker">
          Select date (January 2026):
        </label>
        <input
          id="datePicker"
          type="date"
          value={selectedDate}
          min="2026-01-01"
          max="2026-01-31"
          onChange={(e) => setSelectedDate(e.target.value)}
          className="border rounded p-1"
        />
      </div>
      {loading && <p>Loading data...</p>}
      {!loading && forecastData && actualData && (
        <Dashboard forecast={forecastData.series} actual={actualData.series} />
      )}
      {!loading && metricsData && <MetricsTable metrics={metricsData} />}
    </div>
  );
};

export default App;
