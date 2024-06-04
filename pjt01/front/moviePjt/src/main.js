import './assets/main.css'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()


app.use(router)
pinia.use(piniaPluginPersistedstate)
app.use(pinia)


app.mount('#app')

// createApp(App).mount('#app');

