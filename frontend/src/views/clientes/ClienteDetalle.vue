<template>
  <div>
    <div v-if="cargando" class="flex justify-center items-center py-8">
      <div class="text-gray-600">Cargando datos del cliente...</div>
    </div>

    <div v-else-if="cliente" class="py-4 px-2">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold text-gray-800">
          {{ cliente.nombre }} {{ cliente.apellido }}
        </h1>
        <div class="flex space-x-2">
          <router-link
            :to="`/clientes/${cliente.id}/editar`"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Editar
          </router-link>
          <router-link
            :to="`/cotizaciones/nueva?cliente_id=${cliente.id}`"
            class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Nueva Cotización
          </router-link>
        </div>
      </div>

      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <!-- Información del cliente -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <h3 class="text-lg font-bold text-gray-700 mb-2">Información de Contacto</h3>
            <p class="text-sm mb-1"><span class="font-bold">Email:</span> {{ cliente.email }}</p>
            <p class="text-sm mb-1"><span class="font-bold">Teléfono:</span> {{ cliente.telefono }}</p>
            <p class="text-sm mb-1"><span class="font-bold">Dirección:</span> {{ cliente.direccion }}</p>
            <p class="text-sm"><span class="font-bold">Fecha de registro:</span> {{ formatearFecha(cliente.fecha_registro) }}</p>
          </div>
        </div>

        <!-- Cotizaciones del cliente -->
        <div class="mb-6">
          <h3 class="text-lg font-bold text-gray-700 mb-2">Cotizaciones</h3>
          
          <div v-if="cotizaciones.length === 0" class="text-gray-500 italic">
            Este cliente no tiene cotizaciones.
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="min-w-full bg-white">
              <thead class="bg-gray-100">
                <tr>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="cotizacion in cotizaciones" :key="cotizacion.id" class="hover:bg-gray-50">
                  <td class="py-2 px-3 text-sm">#{{ cotizacion.id }}</td>
                  <td class="py-2 px-3 text-sm">{{ formatearFecha(cotizacion.fecha) }}</td>
                  <td class="py-2 px-3 text-sm">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{
                      'bg-yellow-100 text-yellow-800': cotizacion.estado === 'pendiente',
                      'bg-green-100 text-green-800': cotizacion.estado === 'aprobada',
                      'bg-red-100 text-red-800': cotizacion.estado === 'rechazada'
                    }">
                      {{ cotizacion.estado.charAt(0).toUpperCase() + cotizacion.estado.slice(1) }}
                    </span>
                  </td>
                  <td class="py-2 px-3 text-sm">${{ cotizacion.total.toFixed(2) }}</td>
                  <td class="py-2 px-3 text-sm">
                    <router-link
                      :to="`/cotizaciones/${cotizacion.id}`"
                      class="text-indigo-600 hover:text-indigo-900"
                    >
                      Ver
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Facturas del cliente -->
        <div class="mb-6">
          <h3 class="text-lg font-bold text-gray-700 mb-2">Facturas</h3>
          
          <div v-if="facturas.length === 0" class="text-gray-500 italic">
            Este cliente no tiene facturas.
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="min-w-full bg-white">
              <thead class="bg-gray-100">
                <tr>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Número</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="factura in facturas" :key="factura.id" class="hover:bg-gray-50">
                  <td class="py-2 px-3 text-sm">{{ factura.numero_factura }}</td>
                  <td class="py-2 px-3 text-sm">{{ formatearFecha(factura.fecha_emision) }}</td>
                  <td class="py-2 px-3 text-sm">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{
                      'bg-yellow-100 text-yellow-800': factura.estado_pago === 'pendiente',
                      'bg-green-100 text-green-800': factura.estado_pago === 'pagado',
                      'bg-blue-100 text-blue-800': factura.estado_pago === 'parcial'
                    }">
                      {{ factura.estado_pago.charAt(0).toUpperCase() + factura.estado_pago.slice(1) }}
                    </span>
                  </td>
                  <td class="py-2 px-3 text-sm">
                    <router-link
                      :to="`/facturas/${factura.id}`"
                      class="text-indigo-600 hover:text-indigo-900"
                    >
                      Ver
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Botón volver -->
        <div class="flex justify-start mt-6">
          <button
            @click="$router.push('/clientes')"
            class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Volver a la lista
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <p class="text-red-500">El cliente no existe o no se pudo cargar.</p>
      <button
        @click="$router.push('/clientes')"
        class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Volver a clientes
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { clientesService, cotizacionesService, facturasService } from '../../services/api';

// Router y Route
const router = useRouter();
const route = useRoute();
const toast = useToast();

// Estado
const cliente = ref(null);
const cotizaciones = ref([]);
const facturas = ref([]);
const cargando = ref(true);

// Métodos
const cargarCliente = async () => {
  try {
    cargando.value = true;
    
    // Cargar cliente
    const clienteData = await clientesService.getById(route.params.id);
    cliente.value = clienteData;
    
    // En un sistema completo, aquí cargaríamos las cotizaciones y facturas del cliente
    // Para simplificar, usaremos arrays vacíos
    cotizaciones.value = [];
    facturas.value = [];
    
  } catch (error) {
    toast.error('Error al cargar los datos del cliente');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

const formatearFecha = (fechaStr) => {
  const fecha = new Date(fechaStr);
  return fecha.toLocaleDateString();
};

// Ciclo de vida
onMounted(() => {
  cargarCliente();
});
</script>