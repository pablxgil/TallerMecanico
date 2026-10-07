import { createRouter, createWebHistory } from 'vue-router'
import AuthView from '../views/AuthView.vue'
import DashboardView from '../views/DashboardView.vue'
import CustomersView from '../views/CustomersView.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({ history: createWebHistory(), routes: [{ path: '/', redirect: '/panel' }, { path: '/acceso', component: AuthView, meta: { public: true } }, { path: '/panel', component: DashboardView }, { path: '/clientes', component: CustomersView, meta: { public: true } }] })
router.beforeEach(async (to) => { const auth = useAuthStore(); if (!to.meta.public && !await auth.validateSession()) return '/acceso'; if (to.meta.public && auth.isAuthenticated()) return '/panel' })
export default router

