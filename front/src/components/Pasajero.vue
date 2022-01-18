<template>
  <v-data-table
    :headers="headers"
    :items="pasajeros"
    :search="search"
    class="elevation-1"
    :loading="!pasajeros.length"
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
                        id="pasajero_dni"
                        v-model="newPasajero.dni"
                        type="number"
                        :counter="10"
                        :rules="dniRules"
                        label="DNI del pasajero*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="pasajero_nombre"
                        v-model="newPasajero.nombre"
                        :counter="80"
                        :rules="nombreRules"
                        label="Nombre del pasajero*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="pasajero_apellido"
                        v-model="newPasajero.apellido"
                        :counter="80"
                        :rules="apellidoRules"
                        label="Apellido del pasajero*"
                        required
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
                  @click="addPasajero()"
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
                        id="pasajero_dni"
                        v-model="currentPasajero.dni"
                        type="number"
                        :counter="10"
                        :rules="dniRules"
                        label="DNI del pasajero*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="pasajero_nombre"
                        v-model="currentPasajero.nombre"
                        :counter="80"
                        :rules="nombreRules"
                        label="Nombre del pasajero*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="pasajero_apellido"
                        v-model="currentPasajero.apellido"
                        :counter="80"
                        :rules="apellidoRules"
                        label="Apellido del pasajero*"
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
                <v-btn color="blue darken-1" text @click="updatePasajero()">
                  Guardar
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="getPasajero(item.dni)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deletePasajero(item.dni)"> mdi-delete </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="getPasajeros"> Reset </v-btn>
    </template>
  </v-data-table>
</template>

<script>
  import axios from 'axios'
  export default {
    data: () => ({
      title: 'Pasajeros',
      text: 'Pasajero',
      search: '',
      dialogAdd: false,
      dialogEdit: false,
      headers: [
        { text: 'DNI', value: 'dni' },
        { text: 'Nombres', value: 'nombre' },
        { text: 'Apellido', value: 'apellido' },
        { text: 'Acciones', value: 'actions', sortable: false }
      ],
      pasajeros: [],
      url: 'http://127.0.0.1:8000',
      currentPasajero: {},
      newPasajero: { dni: null, nombre: null, apellido: null },
      valid: true,
      nombreRules: [
        (v) => !!v || 'El nombre es requerido',
        (v) =>
          (v && v.length <= 80) || 'El nombre debe tener menos de 80 caracteres'
      ],
      apellidoRules: [
        (v) => !!v || 'El apellido es requerido',
        (v) =>
          (v && v.length <= 80) ||
          'El apellido debe tener menos de 80 caracteres'
      ],
      dniRules: [
        (v) => !!v || 'El dni es requerido',
        (v) => (v && v.length <= 10) || 'El dni debe tener menos de 10 dígitos'
      ]
    }),

    mounted() {
      this.getPasajeros()
    },

    methods: {
      getPasajeros() {
        axios
          .get(this.url + '/api/pasajero/')
          .then((response) => {
            this.pasajeros = response.data
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getPasajero(id) {
        this.dialogEdit = true
        axios
          .get(this.url + `/api/pasajero/${id}/`)
          .then((response) => {
            this.currentPasajero = response.data
          })
          .catch((err) => {
            console.log(err)
          })
      },
      addPasajero() {
        if (this.$refs.form.validate())
          axios
            .post(this.url + '/api/pasajero/', this.newPasajero)
            .then(() => {
              this.dialogAdd = false
              this.getPasajeros()
              this.newPasajero = {}
            })
            .catch((err) => {
              console.log(err)
            })
      },
      updatePasajero() {
        if (this.$refs.form.validate())
          axios
            .put(
              this.url + `/api/pasajero/${this.currentPasajero.dni}/`,
              this.currentPasajero
            )
            .then((response) => {
              console.log(
                this.url + `/api/pasajero/${this.currentPasajero.dni}/`
              )
              this.currentPasajero = response.data
              this.dialogEdit = false
              this.getPasajeros()
            })
            .catch((err) => {
              console.log(err)
            })
      },
      deletePasajero(id) {
        axios
          .delete(this.url + `/api/pasajero/${id}/`)
          .then((response) => {
            this.getPasajeros()
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
