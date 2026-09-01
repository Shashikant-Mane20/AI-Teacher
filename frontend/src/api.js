const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options)
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || `Request failed with status ${response.status}`)
  return data
}

function authHeaders() {
  const token = localStorage.getItem('ai_teacher_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export const api = {
  register: (payload) => request('/api/v1/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  login: (payload) => request('/api/v1/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  me: () => request('/api/v1/auth/me', { headers: authHeaders() }),
  getProfile: () => request('/api/v1/students/me/profile', { headers: authHeaders() }),
  updateProfile: (payload) => request('/api/v1/students/me/profile', { method: 'PUT', headers: { ...authHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
}
