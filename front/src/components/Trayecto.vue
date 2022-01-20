<template>
  <v-data-table
    :headers="headers"
    :items="trayectos"
    :search="search"
    class="elevation-1"
    :loading="!trayectos.length"
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
                        id="bus_id"
                        v-model="newTrayecto.bus_id"
                        label="id del bus*"
                        :items="placaBus"
                        :rules="selectRules"
                        required
                      ></v-select>
                      <v-text-field
                        id="lugar_partida"
                        v-model="newTrayecto.lugar_partida"
                        label="Lugar de partida*"
                        :counter="50"
                        :rules="lugarPartidaRules"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="lugar_llegada"
                        v-model="newTrayecto.lugar_llegada"
                        label="Lugar de llegada"
                        :counter="50"
                        :rules="lugarLlegadaRules"
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="6">
                      <v-menu
                        v-model="menuDate"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="newTrayecto.date"
                            label="Escoge una fecha"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="newTrayecto.date"
                          @input="menuDate = false"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="6">
                      <v-menu
                        ref="menuTime"
                        v-model="menuTime"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        :return-value.sync="newTrayecto.time"
                        transition="scale-transition"
                        offset-y
                        max-width="290px"
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="newTrayecto.time"
                            label="Escoge la hora"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            :rules="timeRules"
                            required
                          ></v-text-field>
                        </template>
                        <v-time-picker
                          v-if="menuTime"
                          v-model="newTrayecto.time"
                          full-width
                          @click:minute="$refs.menuTime.save(newTrayecto.time)"
                        ></v-time-picker>
                      </v-menu>
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
                  @click="addTrayecto()"
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
                        id="bus_id"
                        v-model="currentTrayecto.bus_id"
                        label="id del bus*"
                        :items="placaBus"
                        :rules="selectRules"
                        required
                      ></v-select>
                      <v-text-field
                        id="lugar_partida"
                        v-model="currentTrayecto.lugar_partida"
                        label="Lugar de partida*"
                        :counter="50"
                        :rules="lugarPartidaRules"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="lugar_llegada"
                        v-model="currentTrayecto.lugar_llegada"
                        label="Lugar de llegada"
                        :counter="50"
                        :rules="lugarLlegadaRules"
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="6">
                      <v-menu
                        v-model="menuDate"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="currentTrayecto.date"
                            label="Escoge una fecha"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="currentTrayecto.date"
                          @input="menuDate = false"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="6">
                      <v-menu
                        ref="menuTime"
                        v-model="menuTime"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        :return-value.sync="currentTrayecto.time"
                        transition="scale-transition"
                        offset-y
                        max-width="290px"
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="currentTrayecto.time"
                            label="Escoge la hora"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            :rules="timeRules"
                            required
                          ></v-text-field>
                        </template>
                        <v-time-picker
                          v-if="menuTime"
                          v-model="currentTrayecto.time"
                          full-width
                          @click:minute="
                            $refs.menuTime.save(currentTrayecto.time)
                          "
                        ></v-time-picker>
                      </v-menu>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeEdit">
                  Cancelar
                </v-btn>
                <v-btn color="blue darken-1" text @click="updateTrayecto()">
                  Guardar
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="getTrayecto(item.id)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deleteTrayecto(item.id)"> mdi-delete </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="getTrayectos"> Reset </v-btn>
    </template>
  </v-data-table>
</template>

<script>
  import axios from 'axios'
  export default {
    data: () => ({
      title: 'Trayectos',
      text: 'Trayecto',
      search: '',
      dialogAdd: false,
      dialogEdit: false,
      headers: [
        { text: 'Bus', value: 'bus.placa' },
        { text: 'Chofer', value: 'bus.chofer.nombre' },
        { text: 'Horario', value: 'horario' },
        { text: 'Lugar de partida', value: 'lugar_partida' },
        { text: 'Lugar de llegada', value: 'lugar_llegada' },
        { text: 'Acciones', value: 'actions', sortable: false }
      ],
      trayectos: [],
      placaBus: [],
      url: 'http://127.0.0.1:8000',
      currentTrayecto: {},
      newTrayecto: {
        bus_id: null,
        horario: null,
        time: null,
        date: null,
        lugar_llegada: null,
        lugar_partida: null
      },
      valid: true,
      date: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      menuDate: false,
      menuTime: false,
      dateTime: [],
      selectRules: [(v) => !!v || 'Es necesario seleccionar un chofer'],
      lugarPartidaRules: [
        (v) => !!v || 'El lugar de partida es requerida',
        (v) =>
          (v && v.length <= 80) ||
          'El lugar de partida debe tener menos de 50 caracteres'
      ],
      lugarLlegadaRules: [
        (v) => !!v || 'El lugar de llegada es requerida',
        (v) =>
          (v && v.length <= 80) ||
          'El lugar de llegada debe tener menos de 50 caracteres'
      ],
      dateRules: [(v) => !!v || 'La fecha es requerida'],
      timeRules: [(v) => !!v || 'La hora es requerida']
    }),

    mounted() {
      this.getTrayectos()
    },

    methods: {
      getTrayectos() {
        axios
          .get(this.url + '/api/trayecto/')
          .then((response) => {
            this.trayectos = response.data
            this.trayectos.map((trayecto) => {
              this.placaBus.push(trayecto.bus.placa)
            })
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getTrayecto(id) {
        this.dialogEdit = true
        axios
          .get(this.url + `/api/trayecto/${id}/`)
          .then((response) => {
            this.currentTrayecto = response.data
            this.currentTrayecto.bus_id = this.currentTrayecto.bus.placa
            this.dateTime = this.currentTrayecto.horario.split(' ')
            this.currentTrayecto.date = this.dateTime[0]
            this.currentTrayecto.time = this.dateTime[1]
          })
          .catch((err) => {
            console.log(err)
          })
      },
      addTrayecto() {
        if (this.$refs.form.validate()) {
          this.newTrayecto.horario =
            this.newTrayecto.date + ' ' + this.newTrayecto.time + ':00'
          delete this.newTrayecto.date
          delete this.newTrayecto.time
          axios
            .post(this.url + '/api/trayecto/', this.newTrayecto)
            .then(() => {
              this.dialogAdd = false
              this.getTrayectos()
              this.newTrayecto = {}
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      updateTrayecto() {
        if (this.$refs.form.validate()) {
          axios
            .put(
              this.url + `/api/trayecto/${this.currentTrayecto.id}/`,
              this.currentTrayecto
            )
            .then((response) => {
              this.currentTrayecto = response.data
              this.dialogEdit = false
              this.getTrayectos()
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      deleteTrayecto(id) {
        axios
          .delete(this.url + `/api/trayecto/${id}/`)
          .then((response) => {
            this.getTrayectos()
            console.log(response)
          })
          .catch((err) => {
            console.log(err)
          })
      },

      closeEdit() {
        this.dialogEdit = false
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
