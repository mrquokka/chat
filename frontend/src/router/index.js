import * as router from 'vue-router'
import login from '../views/login.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: login,
    transition: 'none'
  },
  {
    path: '/register',
    name: 'register',
    component: login,
    transition: 'none'
  },
  {
    path: '/chats',
    name: 'chats',
    component: () => import(
      /* webpackChunkName: "chats" */ '../views/chats.vue'
    )
  }
]

export default router.createRouter({
  history: router.createWebHistory(process.env.BASE_URL),
  routes: routes
})
