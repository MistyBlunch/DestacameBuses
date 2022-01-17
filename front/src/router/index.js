import Vue from 'vue'
import VueRouter from 'vue-router'
import Chofer from '../components/Chofer.vue'
import About from '../components/About.vue'
import Table from '../components/Table.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'About',
    component: About
  },
  {
    path: '/chofer',
    name: 'chofer',
    component: Chofer
  },
  {
    path: '/bus',
    name: 'Bus',
    component: Table
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
