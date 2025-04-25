import { createRouter, createWebHistory } from 'vue-router';
import { useSessionStore } from '../store/session';
import GerenteView from '../views/GerenteView.vue';
import UsuarioView from '../views/UsuarioView.vue';
import LoginForm from '../components/LoginForm.vue';
import AcessoNegado from '../views/AcessoNegado.vue';
import NotFound from '../views/NotFound.vue';

const routes = [
  { path: '/', component: LoginForm },
  {
    path: '/gerente',
    component: GerenteView,
    meta: { requiresAuth: true, role: 'gerente' }
  },
  {
    path: '/usuario',
    component: UsuarioView,
    meta: { requiresAuth: true, role: 'usuario' }
  },
{ path: '/acesso-negado', component: AcessoNegado },
{ path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const session = useSessionStore();

  if (to.meta.requiresAuth) {
    if (!session.token) {
      return next('/');
    }

    if (to.meta.role && session.role !== to.meta.role) {
      return next('/acesso-negado');
    }
  }

  return next();
});

export default router;
