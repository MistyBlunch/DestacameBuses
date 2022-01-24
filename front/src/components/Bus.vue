<template>
  <v-data-table
    :headers="headers"
    :items="buses"
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
                      <v-text-field
                        id="bus_placa"
                        v-model="newBus.placa"
                        :counter="10"
                        :rules="placaRules"
                        label="Placa del bus*"
                        type="number"
                        required
                      ></v-text-field>
                      <v-select
                        id="chofer_id"
                        v-model="newBus.chofer_id"
                        label="Selecciona al chofer*"
                        :items="choferesAddOpts"
                        :rules="selectRules"
                        required
                      ></v-select>
                      <v-text-field
                        id="bus_capacidad"
                        v-model="newBus.capacidad"
                        value="10"
                        type="number"
                        disabled
                      ></v-text-field>
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
                  @click="addBus()"
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
                      <v-text-field
                        id="bus_placa"
                        v-model="currentBus.placa"
                        :counter="10"
                        :rules="placaRules"
                        label="Placa del bus*"
                        required
                      ></v-text-field>
                      <v-select
                        id="chofer_id"
                        v-model="currentBus.chofer_id"
                        label="Selecciona al chofer*"
                        :items="choferesAddOpts"
                        :rules="selectRules"
                        required
                      ></v-select>
                      <v-text-field
                        id="bus_capacidad"
                        v-model="currentBus.capacidad"
                        value="10"
                        type="number"
                        disabled
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeEdit">
                  Cancelar
                </v-btn>
                <v-btn color="blue darken-1" text @click="updateBus()">
                  Guardar
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="getBus(item.id)"> mdi-pencil </v-icon>
      <v-icon small @click="deleteBus(item.id)"> mdi-delete </v-icon>
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
      title: 'Buses',
      text: 'Bus',
      search: '',
      dialogAdd: false,
      dialogEdit: false,
      headers: [
        { text: 'Placa', value: 'placa' },
        { text: 'Chofer', value: 'chofer.dni_nombre' },
        { text: 'Capacidad', value: 'capacidad' },
        { text: 'Acciones', value: 'actions', sortable: false }
      ],
      buses: [],
      choferesAva: [],
      choferesAddOpts: [],
      url: 'http://127.0.0.1:8000',
      currentBus: {},
      newBus: { placa: null, chofer_id: null, capacidad: 10 },
      valid: true,
      loadTable: true,
      selectRules: [(v) => !!v || 'Es necesario seleccionar un chofer'],
      placaRules: [
        (v) => !!v || 'La placa es requerida',
        (v) =>
          (v && v.length <= 80) || 'La placa debe tener menos de 10 caracteres'
      ]
    }),

    mounted() {
      this.getBuses()
    },

    methods: {
      getBuses() {
        axios
          .get(this.url + '/api/chofer-bus/')
          .then((response) => {
            this.buses = response.data
            if (!this.buses) console.log('No hay buses')
            else this.loadTable = false
            this.getChoferesAvailables()
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getChoferesAvailables() {
        axios
          .get(this.url + '/api/choferes-availables/')
          .then((response) => {
            this.choferesAva = response.data.results
            this.choferesAva.map((chofer) => {
              this.choferesAddOpts.push(
                chofer.pk +
                  ' - ' +
                  chofer.fields.nombre +
                  ' ' +
                  chofer.fields.apellido
              )
            })
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getBus(id) {
        this.dialogEdit = true
        axios
          .get(this.url + `/api/bus/${id}/`)
          .then((response) => {
            this.currentBus = response.data
            // Para que aparezca el chofer actual
            this.currentBus.chofer_id =
              this.currentBus.chofer.dni +
              ' - ' +
              this.currentBus.chofer.nombre +
              ' ' +
              this.currentBus.chofer.apellido
            this.choferesAddOpts.push(this.currentBus.chofer_id)
          })
          .catch((err) => {
            console.log(err)
          })
      },
      addBus() {
        if (this.$refs.form.validate()) {
          this.newBus.chofer_id = this.newBus.chofer_id.split(' ')[0]
          axios
            .post(this.url + '/api/bus/', this.newBus)
            .then(() => {
              this.dialogAdd = false
              this.getBuses()
              this.newBus = {}
              this.newBus.capacidad = 10
              this.choferesAddOpts = []
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      updateBus() {
        if (this.$refs.form.validate()) {
          this.currentBus.chofer_id = this.currentBus.chofer.id
          delete this.currentBus.chofer
          axios
            .put(this.url + `/api/bus/${this.currentBus.id}/`, this.currentBus)
            .then((response) => {
              this.currentBus = response.data
              this.dialogEdit = false
              this.getBuses()
              this.choferesAddOpts = []
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      deleteBus(id) {
        axios
          .delete(this.url + `/api/bus/${id}/`)
          .then((response) => {
            this.getBuses()
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
