import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import Main from './components/main.vue';
import Admin from './components/admin.vue';

// Define routes
const routes = [

  { path: '/', component: Main },
  { path: '/admin', component: Admin },
  { path: '/:pathMatch(.*)*', redirect: '/pharmacy-survey' } // Catch all route
];

// Create router instance
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes
});

// Create and mount the Vue app
const app = createApp(App);
app.use(router);
app.mount('#app');