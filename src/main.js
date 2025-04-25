import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import { useSessionStore } from './store/session';

import './style.css';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount('#app');

const session = useSessionStore();
session.loadSessionFromStorage();
