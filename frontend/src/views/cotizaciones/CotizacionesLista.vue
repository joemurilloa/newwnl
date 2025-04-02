<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Cotizaciones</h1>
      <router-link
        to="/cotizaciones/nueva"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Nueva Cotización
      </router-link>
    </div>

    <!-- Filtros -->
    <div class="bg-white shadow-md rounded-lg p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-gray-700 text-sm font-bold mb-2">Estado</label>
          <select
            v-model="filtroEstado"
            @change="aplicarFiltros"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            <option value="">Todos</option>
            <option value="pendiente">Pendiente</option>
            <option value="aprobada">Aprobada</option>
            <option value="rechazada">Rechazada</option>
          </select>
        </div>
        <div>
          <label class="block text-gray-700 text-sm font-bold mb-2">Cliente</label>
          <input
            v-model="filtroCliente"
            @input="aplicarFiltros"
            type="text"
            placeholder="Nombre del cliente"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div class="flex items-end">
          <button
            @click="limpiarFiltros"
            class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Limpiar Filtros
          </button>
        </div>
      </div>
    </div>

    <!-- Lista de cotizaciones -->
    <div v-if="cargando" class="text-center py-8">
      <p class="text-gray-600">Cargando cotizaciones...</p>
    </div>

    <div v-else-if="cotizacionesFiltradas.length === 0" class="text-center py-8">
      <p v-if="filtroEstado || filtroCliente" class="text-gray-600">
        No se encontraron cotizaciones que coincidan con los filtros aplicados.
      </p>
      <p v-else class="text-gray-600">
        No hay cotizaciones registradas. ¡Agrega tu primera cotización!
      </p>
    </div>

    <div v-else class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full">
        <thead class="bg-gray-100">
          <tr>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              ID
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Cliente
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Fecha
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Estado
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Total
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="cotizacion in cotizacionesFiltradas" :key="cotizacion.id" class="hover:bg-gray-50">
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">#{{ cotizacion.id }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ obtenerNombreCliente(cotizacion.cliente_id) }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">{{ formatearFecha(cotizacion.fecha) }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <span class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{
                'bg-yellow-100 text-yellow-800': cotizacion.estado === 'pendiente',
                'bg-green-100 text-green-800': cotizacion.estado === 'aprobada',
                'bg-red-100 text-red-800': cotizacion.estado === 'rechazada'
              }">
                {{ cotizacion.estado.charAt(0).toUpperCase() + cotizacion.estado.slice(1) }}
              </span>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">${{ cotizacion.total.toFixed(2) }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap text-sm font-medium">
              <div class="flex space-x-2">
                <router-link
                  :to="`/cotizaciones/${cotizacion.id}`"
                  class="text-indigo-600 hover:text-indigo-900"
                >
                  Ver
                </router-link>
                <button
                  v-if="cotizacion.estado === 'pendiente'"
                  @click="eliminarCotizacion(cotizacion.id)"
                  class="text-red-600 hover:text-red-900"
                >
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { cotizacionesService, clientesService } from '../../services/api';

// Toast
const toast = useToast();

// Estado
const cotizaciones = ref([]);
const clientes = ref([]);
const cargando = ref(true);
const filtroEstado = ref('');
const filtroCliente = ref('');

// Computed
const cotizacionesFiltradas = computed(() => {
  let resultado = cotizaciones.value;
  
  // Filtrar por estado
  if (filtroEstado.value) {
    resultado = resultado.filter(c => c.estado === filtroEstado.value);
  }
  
  // Filtrar por cliente
  if (filtroCliente.value) {
    const termino = filtroCliente.value.toLowerCase();
    resultado = resultado.filter(c => {
      const cliente = clientes.value.find(cl => cl.id === c.cliente_id);
      if (!cliente) return false;
      
      const nombreCompleto = `${cliente.nombre} ${cliente.apellido}`.toLowerCase();
      return nombreCompleto.includes(termino);
    });
  }
  
  return resultado;
});

// Métodos
const cargarCotizaciones = async () => {
  try {
    cargando.value = true;
    const data = await cotizacionesService.getAll();
    cotizaciones.value = data;
  } catch (error) {
    toast.error('Error al cargar las cotizaciones');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

const cargarClientes = async () => {
  try {
    const data = await clientesService.getAll();
    clientes.value = data;
  } catch (error) {
    toast.error('Error al cargar los clientes');
    console.error(error);
  }
};

const obtenerNombreCliente = (clienteId) => {
  const cliente = clientes.value.find(c => c.id === clienteId);
  return cliente ? `${cliente.nombre} ${cliente.apellido}` : 'Cliente desconocido';
};

const formatearFecha = (fechaStr) => {
  const fecha = new Date(fechaStr);
  return fecha.toLocaleDateString();
};

const aplicarFiltros = () => {
  // Los filtros se aplican automáticamente gracias al computed
};

const limpiarFiltros = () => {
  filtroEstado.value = '';
  filtroCliente.value = '';
};

const eliminarCotizacion = async (id) => {
  if (!confirm('¿Estás seguro de que deseas eliminar esta cotización?')) return;
  
  try {
    await cotizacionesService.delete(id);
    cotizaciones.value = cotizaciones.value.filter(c => c.id !== id);
    toast.success('Cotización eliminada con éxito');
  } catch (error) {
    toast.error('Error al eliminar la cotización');
    console.error(error);
  }
};

// Ciclo de vida
onMounted(() => {
  Promise.all([cargarCotizaciones(), cargarClientes()]);
});
</script>