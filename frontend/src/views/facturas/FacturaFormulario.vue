<template>
  <div>
    <div class="py-4 px-2">
      <h1 class="text-2xl font-bold text-gray-800 mb-4">
        Nueva Factura
      </h1>

      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <form @submit.prevent="crearFactura">
          <!-- Selección de cotización -->
          <div class="mb-4">
            <label for="cotizacion" class="block text-gray-700 text-sm font-bold mb-2">
              Cotización Aprobada
            </label>
            <select
              id="cotizacion"
              v-model="factura.cotizacion_id"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
              @change="cargarDetallesCotizacion"
            >
              <option value="" disabled>Seleccione una cotización</option>
              <option v-for="cotizacion in cotizacionesAprobadas" :key="cotizacion.id" :value="cotizacion.id">
                Cotización #{{ cotizacion.id }} - {{ obtenerNombreCliente(cotizacion.cliente_id) }}
              </option>
            </select>
          </div>

          <!-- Detalles de la cotización seleccionada -->
          <div v-if="cotizacionSeleccionada" class="mb-6 p-4 border rounded bg-gray-50">
            <h3 class="text-lg font-bold text-gray-700 mb-2">Detalles de la Cotización</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <p class="text-sm"><span class="font-bold">Cliente:</span> {{ clienteSeleccionado?.nombre }} {{ clienteSeleccionado?.apellido }}</p>
                <p class="text-sm"><span class="font-bold">Fecha:</span> {{ formatearFecha(cotizacionSeleccionada.fecha) }}</p>
              </div>
              <div>
                <p class="text-sm"><span class="font-bold">Subtotal:</span> ${{ cotizacionSeleccionada.subtotal.toFixed(2) }}</p>
                <p class="text-sm"><span class="font-bold">Impuesto (7%):</span> ${{ cotizacionSeleccionada.impuesto.toFixed(2) }}</p>
                <p class="text-sm font-bold"><span class="font-bold">Total:</span> ${{ cotizacionSeleccionada.total.toFixed(2) }}</p>
              </div>
            </div>
            
            <h4 class="text-md font-bold text-gray-700 mb-1">Ítems</h4>
            <ul class="text-sm">
              <li v-for="(item, index) in cotizacionSeleccionada.items" :key="index" class="mb-1">
                {{ item.descripcion }} - {{ item.cantidad }} {{ item.unidad }} x ${{ item.precio_unitario.toFixed(2) }}
              </li>
            </ul>
          </div>

          <!-- RTN (Número fiscal) -->
          <div class="mb-6">
            <label for="rtn" class="block text-gray-700 text-sm font-bold mb-2">
              Número Fiscal (RTN)
            </label>
            <input
              id="rtn"
              v-model="factura.rtn"
              type="text"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Opcional"
            />
          </div>

          <!-- Botones -->
          <div class="flex items-center justify-between">
            <button
              type="button"
              @click="$router.go(-1)"
              class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              :disabled="cargando || !factura.cotizacion_id"
            >
              {{ cargando ? 'Creando...' : 'Crear Factura' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { clientesService, cotizacionesService, facturasService } from '../../services/api';

// Router
const router = useRouter();
const toast = useToast();

// Estado
const clientes = ref([]);
const cotizacionesAprobadas = ref([]);
const cotizacionSeleccionada = ref(null);
const clienteSeleccionado = ref(null);
const factura = ref({
  cotizacion_id: '',
  rtn: '',
});
const cargando = ref(false);

// Métodos
const cargarClientes = async () => {
  try {
    const clientesData = await clientesService.getAll();
    clientes.value = clientesData;
  } catch (error) {
    toast.error('Error al cargar los clientes');
    console.error(error);
  }
};

const cargarCotizacionesAprobadas = async () => {
  try {
    const cotizacionesData = await cotizacionesService.getAprobadas();
    cotizacionesAprobadas.value = cotizacionesData;
  } catch (error) {
    toast.error('Error al cargar las cotizaciones aprobadas');
    console.error(error);
  }
};

const cargarDetallesCotizacion = async () => {
  if (!factura.value.cotizacion_id) {
    cotizacionSeleccionada.value = null;
    clienteSeleccionado.value = null;
    return;
  }
  
  try {
    const cotizacionData = await cotizacionesService.getById(factura.value.cotizacion_id);
    cotizacionSeleccionada.value = cotizacionData;
    
    // Cargar detalles del cliente
    const clienteData = await clientesService.getById(cotizacionData.cliente_id);
    clienteSeleccionado.value = clienteData;
  } catch (error) {
    toast.error('Error al cargar los detalles de la cotización');
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

const crearFactura = async () => {
  try {
    cargando.value = true;
    
    await facturasService.create(factura.value);
    toast.success('Factura creada con éxito');
    
    router.push('/facturas');
  } catch (error) {
    toast.error('Error al crear la factura');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

// Ciclo de vida
onMounted(() => {
  cargarClientes();
  cargarCotizacionesAprobadas();
});
</script>