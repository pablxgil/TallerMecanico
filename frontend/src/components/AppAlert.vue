<script setup lang="ts">defineProps<{ message: string }>()</script>
<template><v-alert type="error" variant="tonal" density="comfortable" class="mb-4" icon="mdi-alert-circle">{{ message }}</v-alert></template>

