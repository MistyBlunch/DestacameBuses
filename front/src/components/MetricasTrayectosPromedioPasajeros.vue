<template>
  <div class="container">
    <template>
      <v-data-table
        :headers="headers"
        :items="trayectosYPromedios"
        :search="search"
        class="elevation-1"
        :loading="loadTable"
        loading-text="Cargando... Por favor, espere"
        mobile-breakpoint="600"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>{{ title }}</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Buscar"
              single-line
              hide-details
            ></v-text-field>
            <v-spacer></v-spacer>
          </v-toolbar>
        </template>
        <template v-slot:no-data>
          <v-alert outlined color="black" class="mt-4">
            <div>No hay {{ title }}</div>
          </v-alert>
        </template>
      </v-data-table>
    </template>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Métricas',

    data: () => ({
      title: 'Trayectos - Promedio de pasajeros',
      url: 'http://127.0.0.1:8000',
      search: '',
      headers: [
        { text: 'Lugar de partida', value: 'trayectos[0].lugar_partida' },
        { text: 'Lugar de llegada', value: 'trayectos[0].lugar_llegada' },
        { text: 'Cantidad de pasajeros', value: 'cuenta' },
        { text: 'Promedio', value: 'promedio' }
      ],
      loadTable: true,
      trayectosYPromedios: [],
      mapaDeTrayectos: {},
      trayectos: [],
      viajes: []
    }),

    mounted() {
      this.getTrayectosYPromedios()
    },

    methods: {
      async getTrayectosYPromedios() {
        this.trayectos = (await axios.get(this.url + '/api/trayecto/')).data
        this.viajes = (await axios.get(this.url + '/api/viaje/')).data

        for (let trayecto of this.trayectos) {
          let key = trayecto.lugar_partida + trayecto.lugar_llegada
          if (key in this.mapaDeTrayectos) {
            this.mapaDeTrayectos[key].trayectos.push(trayecto)
            continue
          }
          this.mapaDeTrayectos[key] = {
            trayectos: [trayecto],
            cuenta: 0
          }
        }

        for (let viaje of this.viajes) {
          let key = viaje.trayecto.lugar_partida + viaje.trayecto.lugar_llegada
          this.mapaDeTrayectos[key].cuenta++
        }

        for (let key in this.mapaDeTrayectos) {
          let element = this.mapaDeTrayectos[key]
          this.trayectosYPromedios.push({
            trayectos: element.trayectos,
            cuenta: element.cuenta,
            promedio: (
              Math.round((element.cuenta / element.trayectos.length) * 100) /
              100
            ).toFixed(2)
          })
        }

        if (!this.trayectosYPromedios) console.log('No hay choferes')
        else this.loadTable = false

        return this.trayectosYPromedios
      }
    }
  }
</script>
