<template>
  <div class="container">
    <v-img
      max-width="350"
      contain
      :src="imgUrl"
      class="m-auto"
    ></v-img>
    <h4 class="title text-center">{{ title }}</h4>
    <p class="font-weight-regular">
      {{ text }}
    </p>
  </div>
</template>

<script>
  export default {
    name: 'About',

    data: () => ({
      title: 'Sistema de gestión de buses',
      text: 'Te ayudamos a gestionar los viajes de tu empresa para mantener un mapeo de tus choferes, buses, pasajeros y trayectos.',
      imgUrl:
        'https://cdn3d.iconscout.com/3d/premium/thumb/bus-3485081-2914599.png'
    })
  }
</script>
