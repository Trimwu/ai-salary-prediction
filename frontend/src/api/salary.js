import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

export const getOptions = () => api.get('/options')
export const predictSalary = (data) => api.post('/predict', data)
export const getStats = () => api.get('/stats')
