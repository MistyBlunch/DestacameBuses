<template>
  <v-data-table
    :headers="headers"
    :items="choferes"
    :search="search"
    class="elevation-1"
    :loading="!choferes.length"
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
              Nuevo Chofer
            </v-btn>
          </template>
          <v-card>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-card-title>
                <span class="text-h5">Añadir Chofer</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        id="chofer_nombre"
                        v-model="newChofer.nombre"
                        :counter="80"
                        :rules="nombreRules"
                        label="Nombre del chofer*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="chofer_apellido"
                        v-model="newChofer.apellido"
                        :counter="80"
                        :rules="apellidoRules"
                        label="Apellido del chofer*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="chofer_dni"
                        v-model="newChofer.dni"
                        type="number"
                        :counter="10"
                        :rules="dniRules"
                        label="DNI del chofer*"
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
                  @click="addChofer()"
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
                <span class="text-h5">Editar Chofer</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        id="chofer_nombre"
                        v-model="currentChofer.nombre"
                        :counter="80"
                        :rules="nombreRules"
                        label="Nombre del chofer*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="chofer_apellido"
                        v-model="currentChofer.apellido"
                        :counter="80"
                        :rules="apellidoRules"
                        label="Apellido del chofer*"
                        required
                      ></v-text-field>
                      <v-text-field
                        id="chofer_dni"
                        v-model="currentChofer.dni"
                        type="number"
                        :counter="10"
                        :rules="dniRules"
                        label="DNI del chofer*"
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
                <v-btn color="blue darken-1" text @click="updateChofer()">
                  Guardar
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="getChofer(item.dni)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deleteChofer(item.dni)"> mdi-delete </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="getChoferes"> Reset </v-btn>
    </template>
  </v-data-table>
</template>

<script>
  import axios from 'axios'
  export default {
    data: () => ({
      title: 'Buses',
      search: '',
      dialogAdd: false,
      dialogEdit: false,
      headers: [
        { text: 'DNI', value: 'dni' },
        {
          text: 'Nombres',
          value: 'nombre'
        },
        { text: 'Apellido', value: 'apellido' },
        { text: 'Acciones', value: 'actions', sortable: false }
      ],
      choferes: [],
      url: 'http://127.0.0.1:8000',
      currentChofer: {},
      newChofer: { dni: null, nombre: null, apellido: null },
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
      this.getChoferes()
    },

    methods: {
      getChoferes: function () {
        axios
          .get(this.url + '/api/chofer/')
          .then((response) => {
            this.choferes = response.data
          })
          .catch((err) => {
            console.log(err)
          })
      },
      getChofer: function (id) {
        this.dialogEdit = true
        axios
          .get(this.url + `/api/chofer/${id}/`)
          .then((response) => {
            this.currentChofer = response.data
          })
          .catch((err) => {
            console.log(err)
          })
      },
      addChofer: function () {
        if (this.$refs.form.validate())
          axios
            .post(this.url + '/api/chofer/', this.newChofer)
            .then(() => {
              this.dialogAdd = false
              this.getChoferes()
              this.newChofer = {}
            })
            .catch((err) => {
              console.log(err)
            })
      },
      updateChofer: function () {
        if (this.$refs.form.validate())
          axios
            .put(
              this.url + `/api/chofer/${this.currentChofer.dni}/`,
              this.currentChofer
            )
            .then((response) => {
              console.log(this.url + `/api/chofer/${this.currentChofer.dni}/`)
              this.currentChofer = response.data
              this.dialogEdit = false
              this.getChoferes()
            })
            .catch((err) => {
              console.log(err)
            })
      },
      deleteChofer: function (id) {
        axios
          .delete(this.url + `/api/chofer/${id}/`)
          .then((response) => {
            this.getChoferes()
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
