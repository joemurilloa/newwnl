<template>
  <div>
    <div v-if="cargando" class="flex justify-center items-center py-8">
      <div class="text-gray-600">Cargando datos de la factura...</div>
    </div>

    <div v-else-if="factura" class="py-4 px-2">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold text-gray-800">
          Factura #{{ factura.numero_factura }}
        </h1>
        <div class="flex space-x-2">
          <button
            @click="generarPDF"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Descargar PDF
          </button>
          <button
            v-if="factura.estado_pago !== 'pagado'"
            @click="marcarComoPagada"
            class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Marcar como Pagada
          </button>
        </div>
      </div>

      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <!-- Estado -->
        <div class="mb-4">
          <div class="inline-block px-3 py-1 rounded-full" :class="{
            'bg-yellow-100 text-yellow-800': factura.estado_pago === 'pendiente',
            'bg-green-100 text-green-800': factura.estado_pago === 'pagado',
            'bg-blue-100 text-blue-800': factura.estado_pago === 'parcial'
          }">
            {{ estadoTexto }}
          </div>
        </div>

        <!-- Información General -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <h3 class="text-lg font-bold text-gray-700 mb-2">Información General</h3>
            <p class="text-sm"><span class="font-bold">Fecha de emisión:</span> {{ formatearFecha(factura.fecha_emision) }}</p>
            <p class="text-sm"><span class="font-bold">Cliente:</span> {{ cliente?.nombre }} {{ cliente?.apellido }}</p>
            <p class="text-sm"><span class="font-bold">RTN/Número fiscal:</span> {{ factura.rtn || 'No especificado' }}</p>
            <p v-if="factura.fecha_pago" class="text-sm"><span class="font-bold">Fecha de pago:</span> {{ formatearFecha(factura.fecha_pago) }}</p>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-700 mb-2">Información de Contacto</h3>
            <p class="text-sm"><span class="font-bold">Email:</span> {{ cliente?.email }}</p>
            <p class="text-sm"><span class="font-bold">Teléfono:</span> {{ cliente?.telefono }}</p>
            <p class="text-sm"><span class="font-bold">Dirección:</span> {{ cliente?.direccion }}</p>
          </div>
        </div>

        <!-- Información de la Cotización -->
        <div v-if="cotizacion" class="mb-6">
          <h3 class="text-lg font-bold text-gray-700 mb-2">Detalles de la Factura</h3>
          
          <!-- Totales -->
          <div class="bg-gray-50 p-4 rounded mb-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p class="text-sm"><span class="font-bold">Subtotal:</span> ${{ cotizacion.subtotal.toFixed(2) }}</p>
              </div>
              <div>
                <p class="text-sm"><span class="font-bold">Impuesto (7%):</span> ${{ cotizacion.impuesto.toFixed(2) }}</p>
              </div>
              <div>
                <p class="text-sm font-bold"><span class="font-bold">Total:</span> ${{ cotizacion.total.toFixed(2) }}</p>
              </div>
            </div>
          </div>
          
          <!-- Ítems -->
          <div class="overflow-x-auto">
            <table class="min-w-full bg-white">
              <thead class="bg-gray-100">
                <tr>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidad</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Precio Unit.</th>
                  <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subtotal</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="(item, index) in cotizacion.items" :key="index">
                  <td class="py-2 px-3 text-sm">{{ item.descripcion }}</td>
                  <td class="py-2 px-3 text-sm">{{ item.cantidad }}</td>
                  <td class="py-2 px-3 text-sm">{{ item.unidad }}</td>
                  <td class="py-2 px-3 text-sm">${{ item.precio_unitario.toFixed(2) }}</td>
                  <td class="py-2 px-3 text-sm">${{ item.subtotal.toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Notas -->
        <div v-if="cotizacion && cotizacion.notas" class="mb-6">
          <h3 class="text-lg font-bold text-gray-700 mb-2">Notas</h3>
          <p class="text-sm whitespace-pre-line">{{ cotizacion.notas }}</p>
        </div>

        <!-- Botones inferiores -->
        <div class="flex justify-start mt-6">
          <button
            @click="$router.push('/facturas')"
            class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Volver a Facturas
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <p class="text-red-500">La factura no existe o no se pudo cargar.</p>
      <button
        @click="$router.push('/facturas')"
        class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Volver a facturas
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { facturasService, cotizacionesService, clientesService } from '../../services/api';

// Router y Route
const router = useRouter();
const route = useRoute();
const toast = useToast();

// Estado
const factura = ref(null);
const cotizacion = ref(null);
const cliente = ref(null);
const cargando = ref(true);

// Computed
const estadoTexto = computed(() => {
  if (!factura.value) return '';
  
  const estados = {
    'pendiente': 'Pendiente de pago',
    'pagado': 'Pagado',
    'parcial': 'Pago parcial'
  };
  
  return estados[factura.value.estado_pago] || factura.value.estado_pago;
});

// Métodos
const cargarFactura = async () => {
  try {
    cargando.value = true;
    
    // Cargar factura
    const facturaData = await facturasService.getById(route.params.id);
    factura.value = facturaData;
    
    // Cargar cotización asociada
    const cotizacionData = await cotizacionesService.getById(factura.value.cotizacion_id);
    cotizacion.value = cotizacionData;
    
    // Cargar cliente
    const clienteData = await clientesService.getById(factura.value.cliente_id);
    cliente.value = clienteData;
  } catch (error) {
    toast.error('Error al cargar los datos de la factura');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

const formatearFecha = (fechaStr) => {
  if (!fechaStr) return 'N/A';
  const fecha = new Date(fechaStr);
  return fecha.toLocaleDateString();
};

const generarPDF = () => {
  window.open(facturasService.getPdfUrl(factura.value.id), '_blank');
};

const marcarComoPagada = async () => {
  try {
    await facturasService.update(factura.value.id, { estado_pago: 'pagado' });
    
    // Actualizar el estado localmente
    factura.value.estado_pago = 'pagado';
    factura.value.fecha_pago = new Date().toISOString();
    
    toast.success('Factura marcada como pagada');
  } catch (error) {
    toast.error('Error al actualizar el estado de la factura');
    console.error(error);
  }
};

// Ciclo de vida
onMounted(() => {
  cargarFactura();
});
</script>