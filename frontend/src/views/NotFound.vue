<template>
  <div class="flex flex-col items-center justify-center py-16">
    <h1 class="text-6xl font-bold text-gray-800 mb-4">404</h1>
    <p class="text-2xl text-gray-600 mb-8">Página no encontrada</p>
    <p class="text-gray-500 mb-8">La página que estás buscando no existe o ha sido movida.</p>
    <router-link 
      to="/" 
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg"
    >
      Volver al inicio
    </router-link>
  </div>
</template>

<script setup>
// No se requiere lógica adicional
</script>