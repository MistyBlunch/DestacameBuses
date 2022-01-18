<template>
  <v-card class="mx-auto overflow-hidden" height="100vh">
    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list nav dense>
        <v-list-item-group
          v-model="group"
          active-class="deep-purple--text text--accent-4"
          v-for="item in items"
          v-bind:key="item.nameUpper"
        >
          <router-link :to="item.path" class="nav_links">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-menu-right</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{ item.name }}</v-list-item-title>
            </v-list-item>
          </router-link>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar color="deep-purple" dark>
      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <v-app>
          <router-view></router-view>
        </v-app>
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-card>
</template>

<script>
  export default {
    name: 'Home',

    components: {},

    data: () => ({
      title: 'Agencia Minxy',
      items: [
        {
          name: 'home',
          path: '/'
        },
        {
          name: 'chofer',
          path: '/chofer'
        },
        {
          name: 'bus',
          path: '/bus'
        },
        {
          name: 'pasajero',
          path: '/pasajero'
        },
        {
          name: 'trayecto',
          path: '/trayecto'
        }
      ],
      drawer: false,
      group: null
    }),
    filters: {
      uppercase: function (value) {
        if (!value) return ''
        return value.charAt(0).toUpperCase() + value.slice(1)
      }
    }
  }
</script>
<style scoped>
  .nav_links:hover {
    text-decoration: none;
  }
  .nav_links {
    color: inherit;
  }
  .v-list-item--link:before {
    background: transparent;
  }
</style>
