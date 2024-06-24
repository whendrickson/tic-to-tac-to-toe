import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: {
        name: 'login',
      },
    }, {
      component: () => import('../views/AboutView.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - About' },
      name: 'about',
      path: '/about',
    }, {
      component: () => import('../views/ForgotView.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - Forgot' },
      name: 'forgot',
      path: '/forgot',
    }, {
      component: () => import('../views/GameView.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - Game' },
      name: 'game',
      path: '/games/:gameId',
    }, {
      component: () => import('../views/HomeView.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - Home' },
      name: 'home',
      path: '/home',
    }, {
      component: () => import('../views/LoginView.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - Login' },
      name: 'login',
      path: '/login',
    }, {
      component: () => import('../views/LogoutView.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - Logout' },
      name: 'logout',
      path: '/logout',
    }, {
      component: () => import('../views/RegisterView.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - Register' },
      name: 'register',
      path: '/register',
    }, {
      component: () => import('../views/PageNotFound.vue'),
      meta: { title: 'Tic-To-Tac-To-Toe - Page Not Found' },
      path: '/:catchAll(.*)',
      name: 'pageNotFound',
    },
  ],
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Tic-To-Tac-To-Toe';
  next();
});

export default router;
