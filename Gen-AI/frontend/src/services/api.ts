import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to attach auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const searchAPI = {
  searchHotels: (criteria) => api.post('/search/hotels', criteria),
  searchFlights: (criteria) => api.post('/search/flights', criteria),
  searchExperiences: (criteria) => api.post('/search/experiences', criteria),
};

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
};

export const aiAPI = {
  getTravelSuggestions: (params) => api.post('/ai/suggestions', params),
  generateItinerary: (params) => api.post('/ai/itinerary', params),
  getLocalInsights: (params) => api.post('/ai/local-insights', params),
};

export const analyticsAPI = {
  getUserAnalytics: (userId) => api.get(`/analytics/user/${userId}`),
  getSearchAnalytics: () => api.get('/analytics/search'),
};
