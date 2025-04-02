<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Barra de navegación -->
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <router-link to="/" class="text-xl font-bold text-blue-600">
                WNL Remodeling
              </router-link>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="border-transparent text-gray-500 hover:border-blue-500 hover:text-blue-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-blue-500 text-blue-700"
              >
                Inicio
              </router-link>
              <router-link
                to="/clientes"
                class="border-transparent text-gray-500 hover:border-blue-500 hover:text-blue-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-blue-500 text-blue-700"
              >
                Clientes
              </router-link>
              <router-link
                to="/cotizaciones"
                class="border-transparent text-gray-500 hover:border-blue-500 hover:text-blue-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-blue-500 text-blue-700"
              >
                Cotizaciones
              </router-link>
              <router-link
                to="/facturas"
                class="border-transparent text-gray-500 hover:border-blue-500 hover:text-blue-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-blue-500 text-blue-700"
              >
                Facturas
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <router-view></router-view>
    </main>

    <!-- Pie de página -->
    <footer class="bg-white shadow mt-8 py-4">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-gray-500">
          &copy; {{ new Date().getFullYear() }} WNL Remodeling. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Composables y lógica del componente
</script>

<style>
/* Estilos globales */
@import './assets/css/main.css';

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
</style>