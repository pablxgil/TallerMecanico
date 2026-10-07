import type { LoginResponse, Role, User } from '../types/auth'

const baseUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'

export class ApiError extends Error {
  constructor(message: string) { super(message) }
}

async function request<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, { ...init, headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...init.headers } })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const detail = Array.isArray(body.detail) ? body.detail.map((item: { msg: string }) => item.msg).join(' ') : body.detail
    throw new ApiError(detail || 'Ocurrió un error al comunicarse con el servidor.')
  }
  return response.status === 204 ? undefined as T : response.json()
}

export const authApi = {
  register: (data: { full_name: string; email: string; password: string }) => request<User>('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data: { email: string; password: string }) => request<LoginResponse>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  me: (token: string) => request<User>('/auth/me', {}, token),
  changePassword: (data: { current_password: string; new_password: string }, token: string) => request<void>('/auth/change-password', { method: 'POST', body: JSON.stringify(data) }, token)
}

export const usersApi = {
  list: (token: string) => request<User[]>('/users', {}, token),
  updateRole: (id: number, role: Role, token: string) => request<User>(`/users/${id}/role`, { method: 'PATCH', body: JSON.stringify({ role }) }, token)
}

export interface Customer { id: number; full_name: string; email: string; phone: string }
export const customersApi = { list: (token: string) => request<Customer[]>('/customers', {}, token), create: (data: { full_name: string; email: string; phone: string }, token: string) => request<{ id: number }>('/customers', { method: 'POST', body: JSON.stringify(data) }, token) }

