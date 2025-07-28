<template>
  <div>
    <router-view />
  </div>
</template>

<script setup>
import { createRouter, createWebHistory } from 'vue-router';
import main from './components/main.vue';
import admin from './components/admin.vue';

// Define routes
const routes = [
  { path: '/', component: main }, // Default route shows the main component
  { path: '/admin', component: admin }, // Separate path for admin
];

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
});
</script>