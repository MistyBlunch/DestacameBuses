<template>
  <div class="container">
    
    <h5 class="title text-left">{{ title1 }}</h5>
    <p class="font-weight-regular">
      a
    </p>
  </div>
</template>

<script>
  export default {
    name: 'Métricas',

    data: () => ({
      title1: 'Trayectos - Promedio de pasajeros',
      title2: 'Buses de un trayecto - Porcentaje de capacidad v endida',
    })
  }
</script>
