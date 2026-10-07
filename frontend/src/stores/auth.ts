import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '../services/api'
import type { User } from '../types/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('taller_token') || '')
  const user = ref<User | null>(JSON.parse(localStorage.getItem('taller_user') || 'null'))
  const isAuthenticated = () => Boolean(token.value && user.value)
  function saveSession(newToken: string, newUser: User) { token.value = newToken; user.value = newUser; localStorage.setItem('taller_token', newToken); localStorage.setItem('taller_user', JSON.stringify(newUser)) }
  async function login(email: string, password: string) { const result = await authApi.login({ email, password }); saveSession(result.access_token, result.user) }
  function logout() { token.value = ''; user.value = null; localStorage.removeItem('taller_token'); localStorage.removeItem('taller_user') }
  async function validateSession() { if (!token.value) return false; try { user.value = await authApi.me(token.value); localStorage.setItem('taller_user', JSON.stringify(user.value)); return true } catch { logout(); return false } }
  return { token, user, isAuthenticated, login, logout, validateSession }
})

