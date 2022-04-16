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
  // {
  //   path: '/register',
  //   name: 'register',
  //   component: () => import(/* webpackChunkName: "register" */ '../views/register.vue')
  // }
]

export default router.createRouter({
  history: router.createWebHistory(process.env.BASE_URL),
  routes: routes
})
