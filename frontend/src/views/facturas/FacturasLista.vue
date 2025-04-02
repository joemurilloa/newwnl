<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Facturas</h1>
      <router-link
        to="/facturas/nueva"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Nueva Factura
      </router-link>
    </div>

    <!-- Filtros -->
    <div class="bg-white shadow-md rounded-lg p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-gray-700 text-sm font-bold mb-2">Estado de Pago</label>
          <select
            v-model="filtroEstado"
            @change="aplicarFiltros"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            <option value="">Todos</option>
            <option value="pendiente">Pendiente</option>
            <option value="pagado">Pagado</option>
            <option value="parcial">Pago Parcial</option>
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

    <!-- Lista de facturas -->
    <div v-if="cargando" class="text-center py-8">
      <p class="text-gray-600">Cargando facturas...</p>
    </div>

    <div v-else-if="facturasFiltradas.length === 0" class="text-center py-8">
      <p v-if="filtroEstado || filtroCliente" class="text-gray-600">
        No se encontraron facturas que coincidan con los filtros aplicados.
      </p>
      <p v-else class="text-gray-600">
        No hay facturas registradas. Primero debes crear una cotización, aprobarla y luego crear una factura.
      </p>
    </div>

    <div v-else class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full">
        <thead class="bg-gray-100">
          <tr>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Número
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
              RTN
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="factura in facturasFiltradas" :key="factura.id" class="hover:bg-gray-50">
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ factura.numero_factura }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ obtenerNombreCliente(factura.cliente_id) }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">{{ formatearFecha(factura.fecha_emision) }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <span class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{
                'bg-yellow-100 text-yellow-800': factura.estado_pago === 'pendiente',
                'bg-green-100 text-green-800': factura.estado_pago === 'pagado',
                'bg-blue-100 text-blue-800': factura.estado_pago === 'parcial'
              }">
                {{ factura.estado_pago.charAt(0).toUpperCase() + factura.estado_pago.slice(1) }}
              </span>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">{{ factura.rtn || 'N/A' }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap text-sm font-medium">
              <div class="flex space-x-2">
                <router-link
                  :to="`/facturas/${factura.id}`"
                  class="text-indigo-600 hover:text-indigo-900"
                >
                  Ver
                </router-link>
                <button
                  @click="descargarPDF(factura.id)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  PDF
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
import { facturasService, clientesService } from '../../services/api';

// Toast
const toast = useToast();

// Estado
const facturas = ref([]);
const clientes = ref([]);
const cargando = ref(true);
const filtroEstado = ref('');
const filtroCliente = ref('');

// Computed
const facturasFiltradas = computed(() => {
  let resultado = facturas.value;
  
  // Filtrar por estado
  if (filtroEstado.value) {
    resultado = resultado.filter(f => f.estado_pago === filtroEstado.value);
  }
  
  // Filtrar por cliente
  if (filtroCliente.value) {
    const termino = filtroCliente.value.toLowerCase();
    resultado = resultado.filter(f => {
      const cliente = clientes.value.find(cl => cl.id === f.cliente_id);
      if (!cliente) return false;
      
      const nombreCompleto = `${cliente.nombre} ${cliente.apellido}`.toLowerCase();
      return nombreCompleto.includes(termino);
    });
  }
  
  return resultado;
});

// Métodos
const cargarFacturas = async () => {
  try {
    cargando.value = true;
    const data = await facturasService.getAll();
    facturas.value = data;
  } catch (error) {
    toast.error('Error al cargar las facturas');
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

const descargarPDF = (id) => {
  window.open(facturasService.getPdfUrl(id), '_blank');
};

// Ciclo de vida
onMounted(() => {
  Promise.all([cargarFacturas(), cargarClientes()]);
});
</script>