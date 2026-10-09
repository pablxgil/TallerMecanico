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
  changePassword: (data: { current_password: string; new_password: string }, token: string) => request<void>('/auth/change-password', { method: 'POST', body: JSON.stringify(data) }, token),
  requestPasswordReset: (email: string) => request<{ message: string; development_token?: string }>('/auth/password-reset/request', { method: 'POST', body: JSON.stringify({ email }) }),
  confirmPasswordReset: (token: string, newPassword: string) => request<{ message: string }>('/auth/password-reset/confirm', { method: 'POST', body: JSON.stringify({ token, new_password: newPassword }) })
}

export const usersApi = {
  list: (token: string) => request<User[]>('/users', {}, token),
  updateRole: (id: number, role: Role, token: string) => request<User>(`/users/${id}/role`, { method: 'PATCH', body: JSON.stringify({ role }) }, token)
}

export interface Customer { id: number; full_name: string; email: string; phone: string }
export const customersApi = { list: (token: string) => request<Customer[]>('/customers', {}, token), create: (data: { full_name: string; email: string; phone: string }, token: string) => request<{ id: number }>('/customers', { method: 'POST', body: JSON.stringify(data) }, token) }

export interface RoleDefinition { id: number; name: string; description: string | null; status: boolean }
export const administrationApi = {
  listRoles: (token: string) => request<RoleDefinition[]>('/roles', {}, token),
  createRole: (data: { name: string; description?: string }, token: string) => request<RoleDefinition>('/roles', { method: 'POST', body: JSON.stringify(data) }, token),
  updateRoleStatus: (id: number, status: boolean, token: string) => request<RoleDefinition>(`/roles/${id}/status`, { method: 'PATCH', body: JSON.stringify({ status }) }, token),
  createWorkshop: (data: WorkshopPayload, token: string) => request<{ id: number }>('/workshops', { method: 'POST', body: JSON.stringify(data) }, token)
}

export interface WorkshopPayload {
  name: string; rfc: string; email: string; street_number: string; neighborhood: string
  postal_code: string; state: string; municipality: string; photo_url?: string
}

export interface PostalLookup { postal_code: string; state: string; municipality: string; neighborhoods: string[]; neighborhood?: string }
export const addressApi = {
  byPostalCode: (postalCode: string) => request<PostalLookup>(`/address-lookup/${encodeURIComponent(postalCode)}`),
  byAddress: (state: string, municipality: string, neighborhood: string) => request<PostalLookup>(`/address-lookup/by-address?${new URLSearchParams({ state, municipality, neighborhood })}`)
}

