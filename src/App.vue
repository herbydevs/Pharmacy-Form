<template>
  <div>
    <router-view />
  </div>
</template>

<script>
import { createRouter, createWebHistory } from 'vue-router';
import main from './components/main.vue';
import admin from './components/admin.vue';

// Define routes
const routes = [
  { path: '/pharmacy-survey', component: main }, // Main component at /pharmacy-survey
  { path: '/admin', component: admin }, // Admin component at /admin
];

// Create router instance with base URL configuration
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes,
});

export default {
  name: 'App',
  setup() {
    return router;
  }
};
</script>