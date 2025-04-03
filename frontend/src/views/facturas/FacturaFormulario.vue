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
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { clientesService, cotizacionesService, facturasService } from '../../services/api';

// Router
const router = useRouter();
const route = useRoute();
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

onMounted(() => {
  cargarClientes();
  cargarCotizacionesAprobadas().then(() => {
    // Verificar si hay un ID de cotización en los parámetros de la URL
    const cotizacionId = route.query.cotizacion_id;
    if (cotizacionId) {
      // Establecer el ID de cotización
      factura.value.cotizacion_id = parseInt(cotizacionId, 10);
      
      // Cargar detalles de la cotización seleccionada
      cargarDetallesCotizacion();
    }
  });
});
// Vigilar si se pasa un cotizacion_id en la URL (desde CotizacionDetalle)
watch(() => route.query.cotizacion_id, (newCotizacionId) => {
  if (newCotizacionId) {
    factura.value.cotizacion_id = parseInt(newCotizacionId);
    cargarDetallesCotizacion();
  }
}, { immediate: true });

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
    // Obtenemos todas las cotizaciones y filtramos las aprobadas
    // ya que es posible que el endpoint /cotizaciones/aprobadas no exista
    const cotizacionesData = await cotizacionesService.getAll();
    cotizacionesAprobadas.value = cotizacionesData.filter(c => c.estado === 'aprobada');
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
    
    // Validar que se haya seleccionado una cotización
    if (!factura.value.cotizacion_id) {
      toast.error('Debe seleccionar una cotización');
      return;
    }
    
    // Crear objeto de factura con el formato correcto para el backend
    const facturaData = {
      cotizacion_id: factura.value.cotizacion_id,
      rtn: factura.value.rtn || null // Permitir que sea nulo si no se especifica
    };
    
    const response = await facturasService.create(facturaData);
    toast.success('Factura creada con éxito');
    
    // Redirigir a la vista detalle de la factura creada
    router.push(`/facturas/${response.id}`);
  } catch (error) {
    // Mensaje de error más específico según la respuesta del backend
    if (error.response && error.response.data) {
      if (error.response.data.detail === "Esta cotización ya tiene una factura asociada") {
        toast.error('Esta cotización ya tiene una factura asociada');
      } else if (error.response.data.detail === "La cotización debe estar aprobada para generar una factura") {
        toast.error('La cotización debe estar aprobada antes de generar una factura');
      } else {
        toast.error('Error al crear la factura: ' + error.response.data.detail);
      }
    } else {
      toast.error('Error al crear la factura');
    }
    console.error(error);
  } finally {
    cargando.value = false;
  }
};
</script>