<template>
  <div class="container">
    <h5 class="title text-left">{{ title }}</h5>
    <template>
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-select
          v-model="trayectoSelected"
          label="Selecciona un trayecto*"
          :items="trayectos"
          :item-text="(item) => `${item.lugar_partida} - ${item.lugar_llegada}`"
          :rules="trayectosRules"
          required
        ></v-select>
        <v-text-field
          v-model="porcentajeCapacidad"
          type="number"
          label="Porcentaje de capacidad*"
          required
          :rules="porcentajeRules"
        ></v-text-field>

        <v-btn class="mr-4" @click="submit" :disabled="!valid"> Enviar </v-btn>
        <v-btn @click="clear"> clear </v-btn>
      </v-form>
    </template>
    <template v-if="result">
      <v-data-table
        :headers="headers"
        :items="results"
        :search="search"
        class="elevation-1 mt-8"
        :loading="loadTable"
        loading-text="Cargando... Por favor, espere"
        mobile-breakpoint="600"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title
              >{{ titleTable }} del trayecto
              {{ trayectoSelected }}</v-toolbar-title
            >
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
      title: 'Buses de un trayecto - Porcentaje de capacidad vendida',
      titleTable: 'Resultados',
      url: 'http://127.0.0.1:8000',
      valid: true,
      trayectos: [],
      customTrayectos: [],
      trayectoSelected: '',
      porcentajeCapacidad: '',
      results: [],
      search: '',
      headers: [
        { text: 'Placa de bus', value: 'bus.placa' },
        { text: 'Dni del chofer', value: 'bus.chofer.dni' },
        { text: 'Porcentaje de capacidad vendida', value: 'porcentaje' }
      ],
      loadTable: true,
      result: false,
      trayectosRules: [(v) => !!v || 'Es necesario seleccionar los trayectos'],
      porcentajeRules: [
        (v) => !!v || 'El porcentaje es requerido',
        (v) => (v && v.length <= 100) || 'El porcentaje debe ser menor que 100'
      ]
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

        return busesYPorcentajes
      },
      async getTrayectos() {
        this.trayectos = (await axios.get(this.url + '/api/trayecto/')).data
      },
      submit() {
        if (this.$refs.form.validate()) {
          let trayectos = this.trayectoSelected.split(' ')
          let partida = trayectos[0]
          let llegada = trayectos[2]

          for (let trayecto of this.trayectos) {
            if (
              trayecto.lugar_partida == partida &&
              trayecto.lugar_llegada == llegada
            ) {
              this.customTrayectos.push(trayecto)
            }
          }

          let busPorcentaje = this.getBusesYPorcentajes(
            this.customTrayectos,
            this.porcentajeCapacidad
          )

          busPorcentaje
            .then((res) => {
              console.log(res)
              this.results = res
            })
            .catch((err) => {
              console.log(err)
            })

          this.result = true
          this.loadTable = false
        }
      },
      clear() {
        this.trayectoSelected = ''
        this.porcentajeCapacidad = ''
        this.result = false
      },
      validate() {
        this.$refs.form.validate()
      }
    }
  }
</script>
