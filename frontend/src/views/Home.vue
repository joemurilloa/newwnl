<template>
  <div>
    <div class="text-center py-10">
      <h1 class="text-4xl font-bold text-blue-600 mb-4">WNL Remodeling</h1>
      <p class="text-xl text-gray-600 mb-8">Sistema de Gestión de Remodelaciones</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <!-- Tarjeta de Clientes -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="bg-blue-500 p-4">
          <h2 class="text-xl font-bold text-white">Clientes</h2>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4">Gestiona la información de tus clientes de manera eficiente.</p>
          <router-link 
            to="/clientes" 
            class="block text-center bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Ver Clientes
          </router-link>
        </div>
      </div>

      <!-- Tarjeta de Cotizaciones -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="bg-green-500 p-4">
          <h2 class="text-xl font-bold text-white">Cotizaciones</h2>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4">Crea y administra cotizaciones para tus proyectos de remodelación.</p>
          <router-link 
            to="/cotizaciones" 
            class="block text-center bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          >
            Ver Cotizaciones
          </router-link>
        </div>
      </div>

      <!-- Tarjeta de Facturas -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="bg-purple-500 p-4">
          <h2 class="text-xl font-bold text-white">Facturas</h2>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4">Genera facturas a partir de cotizaciones aprobadas.</p>
          <router-link 
            to="/facturas" 
            class="block text-center bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
          >
            Ver Facturas
          </router-link>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Guía rápida</h2>
      
      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 mb-2">1. Gestión de Clientes</h3>
        <p class="text-gray-600">Registra y mantén actualizada la información de tus clientes para facilitar la creación de cotizaciones y facturas.</p>
      </div>
      
      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 mb-2">2. Creación de Cotizaciones</h3>
        <p class="text-gray-600">Crea cotizaciones detalladas para tus clientes, especificando los ítems, cantidades y precios.</p>
      </div>
      
      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 mb-2">3. Aprobación de Cotizaciones</h3>
        <p class="text-gray-600">Cuando un cliente aprueba una cotización, cambia su estado a "aprobada" para proceder con la facturación.</p>
      </div>
      
      <div class="mb-4">
        <h3 class="text-lg font-semibold text-gray-700 mb-2">4. Generación de Facturas</h3>
        <p class="text-gray-600">A partir de una cotización aprobada, genera una factura con la información fiscal correspondiente.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// Script setup para la página de inicio
</script>