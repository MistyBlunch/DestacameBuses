import Vue from 'vue'
import VueRouter from 'vue-router'
import Chofer from '../components/Chofer.vue'
import About from '../components/About.vue'
import Bus from '../components/Bus.vue'
import Pasajero from '../components/Pasajero.vue'
import Trayecto from '../components/Trayecto.vue'

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
    component: Bus
  },
  {
    path: '/pasajero',
    name: 'Pasajero',
    component: Pasajero
  },
  {
    path: '/trayecto',
    name: 'Trayecto',
    component: Trayecto
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
