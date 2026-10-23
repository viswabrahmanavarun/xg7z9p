// src/api.ts
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const fetchForecasts = async (date: string) => {
  const resp = await axios.get(`${BACKEND_URL}/forecasts`, { params: { date } });
  return resp.data; // matches SeriesResponse
};

export const fetchActuals = async (date: string) => {
  const resp = await axios.get(`${BACKEND_URL}/actuals`, { params: { date } });
  return resp.data;
};

export const fetchMetrics = async (date: string) => {
  const resp = await axios.get(`${BACKEND_URL}/metrics`, { params: { date } });
  return resp.data; // matches MetricsResponse
};
