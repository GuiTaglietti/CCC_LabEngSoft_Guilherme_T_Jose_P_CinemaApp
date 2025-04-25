import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import { useSessionStore } from "./store/session";

import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "./theme/theme.scss";
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'bootstrap-icons/font/bootstrap-icons.css';

// import "./style.css"; --> Estava bugando a aplicação por algum motivo

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(ElementPlus);

app.mount("#app");

const session = useSessionStore();
session.loadSessionFromStorage();
