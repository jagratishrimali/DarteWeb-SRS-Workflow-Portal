const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });

  const contentType = response.headers.get('content-type') || '';
  const isJson = contentType.includes('application/json');
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    throw new Error(payload.error || payload.message || 'Request failed');
  }

  return payload;
}

export const api = {
  login: (username, password) => apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  }),

  logout: () => apiRequest('/logout', { method: 'POST' }),
  getMe: () => apiRequest('/me'),

  getProjects: () => apiRequest('/projects'),
  createProject: (data) => apiRequest('/projects', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateProject: (id, data) => apiRequest(`/projects/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteProject: (id) => apiRequest(`/projects/${id}`, { method: 'DELETE' }),
  publishProject: (id) => apiRequest(`/projects/${id}/publish`, { method: 'POST' }),

  getProjectSteps: (projectId) => apiRequest(`/projects/${projectId}/steps`),
  createStep: (data) => apiRequest('/steps', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateStep: (id, data) => apiRequest(`/steps/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteStep: (id) => apiRequest(`/steps/${id}`, { method: 'DELETE' }),
  reorderSteps: (projectId, stepOrder) => apiRequest(`/projects/${projectId}/steps/reorder`, {
    method: 'PUT',
    body: JSON.stringify({ step_order: stepOrder }),
  }),

  submitComment: (data) => apiRequest('/comments', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  getProjectComments: (projectId) => apiRequest(`/projects/${projectId}/comments`),
  getMyComments: () => apiRequest('/comments/my'),
  reviewComment: (commentId, status, adminResponse) => apiRequest(`/comments/${commentId}/review`, {
    method: 'PUT',
    body: JSON.stringify({ status, admin_response: adminResponse }),
  }),

  getMemory: (projectId) => apiRequest(`/memory/${projectId}`),
  exportMemory: (projectId) => `${API_BASE}/memory/${projectId}/export`,
};
