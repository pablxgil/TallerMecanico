<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { ApiError } from '../services/api'
import AppAlert from './AppAlert.vue'
const emit = defineEmits<{ success: []; forgot: [] }>(); const email = ref(''); const password = ref(''); const show = ref(false); const loading = ref(false); const error = ref(''); const form = ref()
async function submit() { const result = await form.value.validate(); if (!result.valid) return; loading.value = true; error.value = ''; try { await useAuthStore().login(email.value, password.value); emit('success') } catch (e) { error.value = e instanceof ApiError ? e.message : 'No fue posible iniciar sesión.' } finally { loading.value = false } }
</script>
<template><v-form ref="form" @submit.prevent="submit"><AppAlert v-if="error" :message="error"/><v-text-field v-model="email" label="Correo electrónico" prepend-inner-icon="mdi-email" :rules="[v => !!v || 'El correo es obligatorio']"/><v-text-field v-model="password" :type="show ? 'text' : 'password'" label="Contraseña" prepend-inner-icon="mdi-lock" :append-inner-icon="show ? 'mdi-eye-off' : 'mdi-eye'" @click:append-inner="show = !show" :rules="[v => !!v || 'La contraseña es obligatoria']"/><v-btn type="submit" color="primary" block :loading="loading">Iniciar sesión</v-btn><div class="text-center mt-3"><v-btn variant="text" color="primary" size="small" @click="emit('forgot')">¿Olvidaste tu contraseña?</v-btn></div></v-form></template>

