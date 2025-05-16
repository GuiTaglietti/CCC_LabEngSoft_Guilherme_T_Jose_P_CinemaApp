import { createRouter, createWebHistory } from "vue-router";
import { useSessionStore } from "../store/session";
import GerenteView from "../views/GerenteView.vue";
import UsuarioView from "../views/UsuarioView.vue";
import LoginForm from "../components/LoginForm.vue";
import AcessoNegado from "../views/AcessoNegado.vue";
import NotFound from "../views/NotFound.vue";
import Register from "../components/Register.vue";
import ForgotPassword from "../components/ForgotPassword.vue";
import CreateMovie from "../components/CreateMovie.vue";
import ManageMovies from "../components/ManageMovies.vue";
import ManageSessions from "../components/ManageSessions.vue";
import ManutençãoMensagem from "../components/ManutençãoMensagem.vue";

const routes = [
  { path: "/login", 
    component: LoginForm 
  },
  {
    path: "/gerente",
    component: GerenteView,
    meta: { requiresAuth: true, role: "gerente" },
  },
  {
    path: "/usuario",
    component: UsuarioView,
    meta: { requiresAuth: true, role: "usuario" },
  },
  {
    path: "/register",
    component: Register,
  },
  {
    path: "/forgot-password",
    component: ForgotPassword,
  },
  {
    path: "/gerente/cadastrar-filme",
    component: CreateMovie,
    meta: { requiresAuth: true, role: "gerente" },
  },
  {
    path: "/gerente/gerenciar-filmes",
    component: ManageMovies,
    meta: { requiresAuth: true, role: "gerente" },
  },
  {
    path: "/gerente/gerenciar-sessoes",
    component: ManageSessions,
    meta: { requiresAuth: true, role: "gerente" },
  },
  {
    path: "/gerente/notificar-manutencao",
    component: ManutençãoMensagem,
    meta: { requiresAuth: true, role: "gerente" },
  },
  { path: "/acesso-negado", 
    component: AcessoNegado 
  },
  { path: "/:pathMatch(.*)*", 
    name: "NotFound", 
    component: NotFound 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const session = useSessionStore();

  if (to.meta.requiresAuth) {
    if (!session.token) {
      return next("/login");
    }

    if (to.meta.role && session.role !== to.meta.role) {
      return next("/acesso-negado");
    }
  }

  return next();
});

export default router;
