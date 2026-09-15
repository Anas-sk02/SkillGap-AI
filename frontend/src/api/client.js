import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL.replace(/\/+$/, '')}/api`
  : '/api'

const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

export const submitProfile = (profile) => api.post('/profile', profile)

export const getSkillGap = (profile) => api.post('/skillgap', profile)

export const getRoadmap = (profile) => api.post('/roadmap', profile)

export const getAllRoles = () => api.get('/roles')

export const getRoleDetail = (roleName) => api.get(`/roles/${encodeURIComponent(roleName)}`)

export const updateProgress = (progressData) => api.post('/progress', progressData)

export const fetchProgress = (studentId, roleName) =>
  api.get(`/progress/${encodeURIComponent(studentId)}/${encodeURIComponent(roleName)}`)

export default api
