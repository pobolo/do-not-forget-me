import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const wealthAPI = {
  // Health check
  healthCheck: () => api.get('/health'),

  // Statistics
  getStats: () => api.get('/stats'),

  // Individual CRUD operations
  createIndividual: (data) => api.post('/individuals', data),
  getAllIndividuals: () => api.get('/individuals'),
  getIndividual: (id) => api.get(`/individuals/${id}`),
  updateIndividual: (id, data) => api.put(`/individuals/${id}`, data),
  deleteIndividual: (id) => api.delete(`/individuals/${id}`),

  // Query operations
  getWealthRanking: (limit = 10) => api.get(`/individuals/ranking?limit=${limit}`),
  getIndividualsByIndustry: (industry) => api.get(`/individuals/industry/${industry}`),
  searchIndividuals: (query) => api.get(`/individuals/search?q=${encodeURIComponent(query)}`),
};

export default api;