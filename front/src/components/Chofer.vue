<template>
  <div id="chofer">
    <div class="container">
      <div class="row">
        <template>
          <div class="text-center">
            <v-dialog v-model="dialog_add" width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="blue-grey darken-4" dark v-bind="attrs" v-on="on">
                  Añadir Chofer
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                  Añadir Chofer
                </v-card-title>

                <v-card-text>
                  <v-form lazy-validation>
                    <v-container>
                      <v-row>
                        <v-col cols="12">
                          <v-text-field
                            id="chofer_nombre"
                            v-model="newChofer.nombre"
                            label="Nombre del chofer*"
                            required
                          ></v-text-field>
                          <v-text-field
                            id="chofer_apellido"
                            v-model="newChofer.apellido"
                            label="Apellido del chofer*"
                            required
                          ></v-text-field>
                          <v-text-field
                            id="chofer_dni"
                            v-model="newChofer.dni"
                            label="DNI del chofer*"
                            required
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-form>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="dialog_add = false">
                    Close
                  </v-btn>
                  <v-btn
                    type="submit"
                    color="blue darken-1"
                    text
                    @click="addChofer()"
                  >
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
          <div class="loading" v-if="loading === true">Loading&#8230;</div>
        </template>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Heading</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="chofer in choferes" v-bind:key="chofer.dni">
              <th scope="row">{{ chofer.dni }}</th>
              <td>{{ chofer.nombre + ' ' + chofer.apellido }}</td>
              <td>
                <template>
                  <div class="d-flex">
                    <v-btn
                      class="mx-2"
                      fab
                      dark
                      small
                      color="pink"
                      v-on:click="getChofer(chofer.dni)"
                    >
                      <v-icon dark> mdi-pencil </v-icon>
                    </v-btn>
                    <v-btn
                      class="mx-2"
                      fab
                      dark
                      small
                      color="pink"
                      v-on:click="deleteChofer(chofer.dni)"
                    >
                      <v-icon dark> mdi-delete </v-icon>
                    </v-btn>
                  </div>
                </template>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="text-center d-flex">
          <v-dialog v-model="dialog_edit" width="600">
            <v-card>
              <v-card-title class="text-h5 grey lighten-2">
                Editar Chofer
              </v-card-title>

              <v-card-text>
                <v-form>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          id="chofer_nombre"
                          v-model="currentChofer.nombre"
                          label="Nombre del chofer*"
                          required
                        ></v-text-field>
                        <v-text-field
                          id="chofer_apellido"
                          v-model="currentChofer.apellido"
                          label="Apellido del chofer*"
                          required
                        ></v-text-field>
                        <v-text-field
                          id="chofer_dni"
                          v-model="currentChofer.dni"
                          label="DNI del chofer*"
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-form>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="dialog_edit = false">
                  Close
                </v-btn>
                <v-btn
                  type="submit"
                  color="blue darken-1"
                  text
                  @click="updateChofer()"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
        <div class="loading" v-if="loading === true">Loading&#8230;</div>
      </div>
    </div>
    <div class="loading" v-if="loading === true">Loading&#8230;</div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'chofer',
    data() {
      return {
        url: 'http://127.0.0.1:8000',
        choferes: [],
        loading: false,
        currentChofer: {},
        newChofer: { dni: null, nombre: null, apellido: null },
        dialog_add: false,
        dialog_edit: false
      }
    },
    mounted: function () {
      this.getChoferes()
    },
    methods: {
      getChoferes: function () {
        console.log(this.url + '/api/chofer/')
        this.loading = true
        axios
          .get(this.url + '/api/chofer/')
          .then((response) => {
            console.log('response', response)
            this.choferes = response.data
            this.loading = false
          })
          .catch((err) => {
            this.loading = false
            console.log(err)
          })
      },
      getChofer: function (id) {
        this.loading = true
        this.dialog_edit = true
        axios
          .get(this.url + `/api/chofer/${id}/`)
          .then((response) => {
            this.currentChofer = response.data
            this.loading = false
          })
          .catch((err) => {
            this.loading = false
            console.log(err)
          })
      },
      addChofer: function () {
        this.loading = true
        axios
          .post(this.url + '/api/chofer/', this.newChofer)
          .then(() => {
            this.loading = false
            this.dialog_add = false
            this.getChoferes()
          })
          .catch((err) => {
            this.loading = false
            console.log(err)
          })
      },
      updateChofer: function () {
        this.loading = true
        axios
          .put(
            this.url + `/api/chofer/${this.currentChofer.dni}/`,
            this.currentChofer
          )
          .then((response) => {
            this.loading = false
            this.currentChofer = response.data
            this.dialog_edit = false
            this.getChoferes()
          })
          .catch((err) => {
            this.loading = false
            console.log(err)
          })
      },
      deleteChofer: function (id) {
        this.loading = true
        axios
          .delete(this.url + `/api/chofer/${id}/`)
          .then((response) => {
            this.loading = false
            this.getChoferes()
            console.log(response)
          })
          .catch((err) => {
            this.loading = false
            console.log(err)
          })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h3 {
    margin: 40px 0 0;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
</style>
