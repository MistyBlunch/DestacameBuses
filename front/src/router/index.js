import Vue from 'vue'
import VueRouter from 'vue-router'
import Chofer from '../components/Chofer.vue'
import About from '../components/About.vue'
import Bus from '../components/Bus.vue'
import Pasajero from '../components/Pasajero.vue'
import Trayecto from '../components/Trayecto.vue'
import Viajes from '../components/Viajes.vue'
import Metricas from '../components/Metricas.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'About',
    component: About
  },
  {
    path: '/choferes',
    name: 'choferes',
    component: Chofer
  },
  {
    path: '/buses',
    name: 'Buses',
    component: Bus
  },
  {
    path: '/pasajeros',
    name: 'Pasajeros',
    component: Pasajero
  },
  {
    path: '/trayectos',
    name: 'Trayectos',
    component: Trayecto
  },
  {
    path: '/viajes',
    name: 'Viajes',
    component: Viajes
  },
  {
    path: '/metricas',
    name: 'Metricas',
    component: Metricas
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
