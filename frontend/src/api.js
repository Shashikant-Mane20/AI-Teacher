const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options)
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || `Request failed with status ${response.status}`)
  return data
}

export const api = {
  health: () => request('/health'),
  createStudent: (payload) => request('/api/v1/students/create', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  getStudent: (id) => request(`/api/v1/students/${id}/profile`),
  createLesson: (payload) => request('/api/v1/lessons/create', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  getLesson: (id) => request(`/api/v1/lessons/${id}`),
  lessonAction: (id, action) => request(`/api/v1/lessons/${id}/${action}`, { method: 'POST' }),
  createQuestion: (lessonId, payload) => request(`/api/v1/lessons/${lessonId}/question`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  submitAnswer: (lessonId, payload) => request(`/api/v1/lessons/${lessonId}/answer`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  evaluateAnswer: (lessonId, payload) => request(`/api/v1/lessons/${lessonId}/evaluate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  continueLesson: (id) => request(`/api/v1/lessons/${id}/continue`, { method: 'POST' }),
  generateAssessment: (payload) => request('/api/v1/assessments/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  uploadDocument: (formData) => request('/api/v1/documents/upload', { method: 'POST', body: formData }),
  getDocument: (id) => request(`/api/v1/documents/${id}`),
  generateVideo: (payload) => request('/api/v1/video/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
}

export function openLessonSocket(lessonId, onMessage, onError) {
  const socket = new WebSocket(`${API_URL.replace(/^http/, 'ws')}/ws/lesson/${lessonId}`)
  socket.addEventListener('open', () => socket.send('START_LESSON'))
  socket.addEventListener('close', () => onError?.())
  socket.addEventListener('message', (event) => onMessage(event.data))
  socket.addEventListener('error', onError)
  return socket
}
