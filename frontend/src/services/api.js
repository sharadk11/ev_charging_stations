import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// API functions
export const getStations = async (params = {}) => {
  try {
    const response = await api.get('/stations', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching stations:', error);
    throw error;
  }
};

export const getStation = async (stationId) => {
  try {
    const response = await api.get(`/stations/${stationId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching station:', error);
    throw error;
  }
};

export const searchStations = async (searchParams) => {
  try {
    const response = await api.post('/stations/search', searchParams);
    return response.data;
  } catch (error) {
    console.error('Error searching stations:', error);
    throw error;
  }
};

export const getNearbyStations = async (lat, lng, radius = 10, limit = 50) => {
  try {
    const response = await api.get('/stations/nearby', {
      params: { lat, lng, radius, limit }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearby stations:', error);
    throw error;
  }
};

export const getStats = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};