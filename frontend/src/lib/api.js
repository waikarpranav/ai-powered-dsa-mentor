import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 60000, // 60s — LLM calls can be slow
});

export const getProblems = () => API.get('/problems');
export const getProblem = (slug) => API.get(`/problems/${slug}`);
export const analyzeCode = (data) => API.post('/analyze', data);
export const getSubmissions = (sessionId) => API.get(`/submissions/${sessionId}`);
export const getRecommendations = (sessionId) => API.get(`/recommendations/${sessionId}`);
export const healthCheck = () => API.get('/health');

export default API;
