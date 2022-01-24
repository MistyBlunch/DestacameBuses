<template>
  <div class="container">
    <h5 class="title text-left">{{ title }}</h5>
    <v-select
      id="chofer_id"
      v-model="newBus.chofer_id"
      label="Selecciona al chofer*"
      :items="choferesAddOpts"
      :rules="selectRules"
      required
    ></v-select>
    <v-select>
      <template slot="selection" slot-scope="trayectos">
        <!-- HTML that describe how select should render selected items -->
        {{ trayectos.lugar_partida }} - {{ trayectos.lugar_llegada }}
      </template>
      <template slot="item" slot-scope="trayectos">
        <!-- HTML that describe how select should render items when the select is open -->
        {{ trayectos.item.lugar_partida }} - {{ trayectos.item.lugar_llegada }}
      </template>
    </v-select>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Métricas',

    data: () => ({
      title: 'Buses de un trayecto - Porcentaje de capacidad vendida',
      url: 'http://127.0.0.1:8000',
      trayectos: [],
      customTrayectos: []
    }),

    mounted() {
      this.getTrayectos()
    },

    methods: {
      async getBusesYPorcentajes(trayectos, n) {
        let viajes = (await axios.get(this.url + '/api/viaje/')).data
        let trayectosIds = []
        let trayectosYBuses = {}
        let busesYPorcentajes = []

        for (let trayecto of trayectos) {
          trayectosIds.push(trayecto.id)
          trayectosYBuses[trayecto.id] = {
            trayecto: trayecto,
            bus: {
              bus: trayecto.bus,
              capacidadLlena: 0
            }
          }
        }

        for (let viaje of viajes) {
          if (trayectosIds.includes(viaje.trayecto.id)) {
            trayectosYBuses[viaje.trayecto.id].bus.capacidadLlena++
          }
        }

        for (let key in trayectosYBuses) {
          let trayectoYBus = trayectosYBuses[key]
          if (trayectoYBus.bus.capacidadLlena * 10 > n) {
            busesYPorcentajes.push({
              bus: trayectoYBus.bus.bus,
              porcentaje: trayectoYBus.bus.capacidadLlena * 10
            })
          }
        }

        // console.log(busesYPorcentajes)

        return busesYPorcentajes
      },
      async getTrayectos() {
        this.trayectos = (await axios.get(this.url + '/api/trayecto/')).data
        console.log(this.trayectos)

        for (let trayecto of this.trayectos) {
          if (
            trayecto.lugar_partida == 'Lima' &&
            trayecto.lugar_llegada == 'Cusco'
          ) {
            this.customTrayectos.push(trayecto)
          }
        }

        this.getBusesYPorcentajes(this.customTrayectos, 20)
      }
    }
  }
</script>
