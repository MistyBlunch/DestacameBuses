<template>
  <v-data-table
    :headers="headers"
    :items="viajes"
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
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-dialog v-model="dialogAdd" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="secondary" dark class="mb-2" v-bind="attrs" v-on="on">
              Nuevo {{ text }}
            </v-btn>
          </template>
          <v-card>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-card-title>
                <span class="text-h5">Añadir {{ text }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-select
                        v-model="newViaje.pasajero_id"
                        label="Seleccione al pasajero*"
                        :items="pasajerosOpts"
                        item-value="id"
                        item-text="nombre"
                        :rules="pasajeroRules"
                        required
                      ></v-select>
                      <v-select
                        @change="onTrayectoSelected($event)"
                        v-model="newViaje.trayecto_id"
                        label="Seleccione el trayecto*"
                        :items="trayectoPartidaDestino"
                        item-value="id"
                        item-text="partidaDestino"
                        :rules="trayectoRules"
                        required
                        return-object
                      ></v-select>
                      <v-select
                        @change="onTrayectoHorario($event)"
                        v-model="newViaje.horario"
                        label="Seleccione el horario*"
                        :items="trayectoHoras"
                        item-value="id"
                        item-text="horario"
                        :rules="horarioRules"
                        required
                      ></v-select>
                      <v-text-field
                        v-model="newViaje.trayecto_bus"
                        value="trayecto_bus"
                        label="Placa del bus"
                        required
                        disabled
                      ></v-text-field>
                      <v-select
                        @change="onTrayectoAsientos($event)"
                        v-model="newViaje.asiento_id"
                        label="Seleccione el asiento*"
                        :items="asientosOpts"
                        item-value="id"
                        item-text="numero"
                        :rules="asientoRules"
                        required
                        return-object
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeAdd">
                  Cancelar
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="addViaje()"
                  :disabled="!valid"
                >
                  Guardar
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogEdit" max-width="500px">
          <v-card>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-card-title>
                <span class="text-h5">Editar {{ text }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-select
                        v-model="currentViaje.pasajero_id"
                        label="Seleccione al pasajero*"
                        :items="pasajerosOpts"
                        item-value="id"
                        item-text="nombre"
                        :rules="pasajeroRules"
                        required
                      ></v-select>
                      <v-select
                        @change="onTrayectoSelected($event)"
                        v-model="currentViaje.trayecto_id"
                        label="Seleccione el trayecto*"
                        :items="trayectoPartidaDestino"
                        item-value="id"
                        item-text="partidaDestino"
                        :rules="trayectoRules"
                        required
                        return-object
                      ></v-select>
                      <v-select
                        @change="onTrayectoHorario($event)"
                        v-model="currentViaje.horario"
                        label="Seleccione el horario*"
                        :items="trayectoHoras"
                        item-value="id"
                        item-text="horario"
                        :rules="horarioRules"
                        required
                      ></v-select>
                      <v-text-field
                        v-model="currentViaje.trayecto_bus"
                        value="trayecto_bus"
                        label="Placa del bus"
                        required
                        disabled
                      ></v-text-field>
                      <v-select
                        @change="onTrayectoAsientos($event)"
                        v-model="currentViaje.asiento_id"
                        label="Seleccione el asiento*"
                        :items="asientosOpts"
                        item-value="id"
                        item-text="numero"
                        :rules="asientoRules"
                        required
                        return-object
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeEdit">
                  Cancelar
                </v-btn>
                <v-btn color="blue darken-1" text @click="updateViaje()">
                  Guardar
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="getViaje(item.id)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deleteViaje(item)"> mdi-delete </v-icon>
    </template>
    <template v-slot:no-data>
      <v-alert outlined color="black" class="mt-4">
        <div>No hay {{ title }}</div>
      </v-alert>
    </template>
  </v-data-table>
</template>

<script>
  import axios from 'axios'
  export default {
    data: () => ({
      title: 'Viajes',
      text: 'Viaje',
      search: '',
      dialogAdd: false,
      dialogEdit: false,
      headers: [
        { text: 'Pasajero', value: 'pasajero.dni_nombre' },
        { text: 'Lugar de Partida', value: 'trayecto.lugar_partida' },
        { text: 'Lugar de Llegada', value: 'trayecto.lugar_llegada' },
        { text: 'Horario', value: 'trayecto.horario' },
        { text: 'Placa de bus', value: 'trayecto.bus.placa' },
        { text: 'N° Asiento', value: 'asiento.numero' },
        { text: 'Acciones', value: 'actions', sortable: false }
      ],
      viajes: [],
      pasajeros: [],
      pasajerosOpts: [],
      trayectos: [],
      trayectoPartidaDestino: [],
      trayectoHoras: [],
      trayectosByHoras: [],
      trayectoBuses: [],
      asientos: [],
      asientosOpts: [],
      asientoData: {},
      asientoCurrentId: '',
      asientoCurrentNumero: '',
      url: 'http://127.0.0.1:8000',
      currentViaje: {},
      newViaje: {
        created: null,
        pasajero_id: null,
        trayecto_id: null,
        asiento_id: null
      },
      valid: true,
      loadTable: true,
      pasajeroRules: [(v) => !!v || 'Es necesario seleccionar un pasajero'],
      trayectoRules: [(v) => !!v || 'Es necesario seleccionar un trayecto'],
      horarioRules: [(v) => !!v || 'Es necesario seleccionar un horario'],
      asientoRules: [(v) => !!v || 'Es necesario seleccionar un asiento']
    }),

    mounted() {
      this.getViajes()
    },

    methods: {
      getViajes() {
        axios
          .get(this.url + '/api/viajes-details/')
          .then((response) => {
            this.viajes = response.data
            if (!this.viajes) console.log('No hay viajes')
            else this.loadTable = false
            this.getPasajeros()
            this.getTrayectos()
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getPasajeros() {
        axios
          .get(this.url + '/api/pasajero/')
          .then((response) => {
            this.pasajeros = response.data
            this.pasajeros.map((pasajero) => {
              this.pasajerosOpts.push({
                id: pasajero.id,
                nombre:
                  pasajero.dni +
                  ' - ' +
                  pasajero.nombre +
                  ' ' +
                  pasajero.apellido
              })
            })
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getTrayectos() {
        axios
          .get(this.url + '/api/trayectos-details/')
          .then((response) => {
            this.trayectos = response.data.trayectos_distinct
            this.trayectos.map((trayecto) => {
              this.trayectoPartidaDestino.push({
                id: trayecto.id,
                partidaDestino: trayecto.partida_destino
              })
            })
          })
          .catch((err) => {
            console.log(err)
          })
      },
      onTrayectoSelected(event) {
        let lugares = event.partidaDestino.split(' ')
        let partida = lugares[0]
        let llegada = lugares[2]
        this.getTrayectoByPartidaLlegada(partida, llegada)
      },
      getTrayectoByPartidaLlegada(partida, llegada) {
        axios
          .get(
            this.url +
              `/api/trayectos-partida-llegada-horas/${partida}&${llegada}/`
          )
          .then((response) => {
            this.trayectoHoras = response.data.results
          })
          .catch((err) => {
            console.log(err)
          })
      },
      onTrayectoHorario(event) {
        this.getTrayecto(event)
      },
      getTrayecto(id) {
        axios
          .get(this.url + `/api/trayecto/${id}/`)
          .then((response) => {
            let data = response.data.bus
            this.newViaje.trayecto_bus = data.placa
            this.asientoData.bus = data.id
            this.getAsientos(data.id)
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getAsientos(id) {
        axios
          .get(this.url + `/api/asientos-availables/${id}/`)
          .then((response) => {
            this.asientos = response.data
            this.asientos.sort((a, b) => {
              if (a.numero < b.numero) {
                return -1
              }
              if (a.numero > b.numero) {
                return 1
              }
              return 0
            })
            this.asientos.map((asiento) => {
              this.asientosOpts.push({ id: asiento.id, numero: asiento.numero })
            })
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getViaje(id) {
        this.dialogEdit = true
        axios
          .get(this.url + `/api/viaje/${id}/`)
          .then((response) => {
            this.currentViaje = response.data
            this.currentViaje.pasajero_id = this.currentViaje.pasajero.id
            this.currentViaje.trayecto_id = this.currentViaje.trayecto.id
            this.getTrayectoByPartidaLlegada(
              this.currentViaje.trayecto.lugar_partida,
              this.currentViaje.trayecto.lugar_llegada
            )
            this.getTrayecto(this.currentViaje.trayecto.id)
            this.currentViaje.horario = this.currentViaje.trayecto.id
            this.currentViaje.trayecto_bus =
              this.currentViaje.trayecto.bus.placa

            this.asientosOpts.push({
              id: this.currentViaje.asiento.id,
              numero: this.currentViaje.asiento.numero
            })

            this.asientoCurrentId = this.currentViaje.asiento.id
            this.asientoCurrentNumero = this.currentViaje.asiento.numero

            this.currentViaje.asiento_id = this.currentViaje.asiento.id

            delete this.currentViaje.asiento
            delete this.currentViaje.pasajero
            delete this.currentViaje.trayecto
          })
          .catch((err) => {
            console.log(err)
          })
      },
      // get time
      getCurrentTime() {
        let currentdate = new Date()
        return (
          currentdate.getFullYear() +
          '-' +
          (currentdate.getMonth() + 1) +
          '-' +
          currentdate.getDate() +
          ' ' +
          currentdate.getHours() +
          ':' +
          currentdate.getMinutes() +
          ':' +
          currentdate.getSeconds()
        )
      },
      onTrayectoAsientos(event) {
        this.asientoData.id = event.id
        this.asientoData.numero = event.numero
      },
      addViaje() {
        if (this.$refs.form.validate()) {
          this.newViaje.created = this.getCurrentTime()
          this.newViaje.trayecto_id = this.newViaje.trayecto_id.id
          this.newViaje.asiento_id = this.newViaje.asiento_id.id

          this.asientoData.ocupado = true

          delete this.newViaje.horario
          delete this.newViaje.trayecto_bus

          axios
            .post(this.url + '/api/viaje/', this.newViaje)
            .then(() => {
              this.dialogAdd = false
              this.getViajes()
              this.updateAsiento()
              this.newViaje = {}
              this.asientoData = {}
              this.asientosOpts = []
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      updateViaje() {
        if (this.$refs.form.validate()) {
          delete this.currentViaje.trayecto_bus
          delete this.currentViaje.horario

          this.asientoData.id = this.asientoCurrentId
          this.asientoData.numero = this.asientoCurrentNumero
          this.asientoData.ocupado = false

          this.updateAsiento()

          this.currentViaje.asiento_id = this.currentViaje.asiento_id.id
          axios
            .put(
              this.url + `/api/viaje/${this.currentViaje.id}/`,
              this.currentViaje
            )
            .then((response) => {
              this.currentViaje = response.data
              this.asientoData.id = this.currentViaje.asiento.id
              this.asientoData.numero = this.currentViaje.asiento.numero
              this.asientoData.ocupado = true

              this.updateAsiento()
              this.dialogEdit = false
              this.getViajes()
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      updateAsiento() {
        axios
          .put(
            this.url + `/api/asiento/${this.asientoData.id}/`,
            this.asientoData
          )
          .then((response) => {
            this.currentViaje = response.data
            this.dialogEdit = false
          })
          .catch((err) => {
            console.log(err)
          })
      },
      deleteViaje(id) {
        this.asientoData.id = id.asiento.id
        this.asientoData.numero = id.asiento.numero
        this.asientoData.ocupado = false
        this.asientoData.bus = id.asiento.bus.id
        axios
          .delete(this.url + `/api/viaje/${id.id}/`)
          .then((response) => {
            this.getViajes()
            this.updateAsiento()
            console.log(response)
          })
          .catch((err) => {
            console.log(err)
          })
      },
      closeEdit() {
        this.dialogEdit = false
        this.newViaje.trayecto_bus = ''
      },
      closeAdd() {
        this.dialogAdd = false
      },
      validate() {
        this.$refs.form.validate()
      }
    }
  }
</script>
