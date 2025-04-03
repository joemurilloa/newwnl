<template>
  <div>
    <div v-if="cargando" class="flex justify-center items-center py-8">
      <div class="text-gray-600">Cargando datos...</div>
    </div>

    <div v-else-if="cotizacion" class="py-4 px-2">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold text-gray-800">
          Cotización #{{ cotizacion.id }}
        </h1>
        <div class="flex space-x-2">
          <button
            @click="generarPDF"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Descargar PDF
          </button>
          <button
            v-if="cotizacion.estado === 'pendiente'"
            @click="cambiarEstado('aprobada')"
            class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Aprobar
          </button>
          <button
            v-if="cotizacion.estado === 'pendiente'"
            @click="cambiarEstado('rechazada')"
            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Rechazar
          </button>
          <button
            v-if="cotizacion.estado === 'aprobada' && !tieneFactura"
            @click="crearFactura"
            class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Crear Factura
          </button>
        </div>
      </div>

      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <!-- Estado -->
        <div class="mb-4">
          <div class="inline-block px-3 py-1 rounded-full" :class="{
            'bg-yellow-100 text-yellow-800': cotizacion.estado === 'pendiente',
            'bg-green-100 text-green-800': cotizacion.estado === 'aprobada',
            'bg-red-100 text-red-800': cotizacion.estado === 'rechazada'
          }">
            {{ estadoTexto }}
          </div>
        </div>

        <!-- Información General -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <h3 class="text-lg font-bold text-gray-700 mb-2">Información General</h3>
            <p class="text-sm"><span class="font-bold">Fecha:</span> {{ formatearFecha(cotizacion.fecha) }}</p>
            <p class="text-sm"><span class="font-bold">Cliente:</span> {{ cliente?.nombre }} {{ cliente?.apellido }}</p>
            <p class="text-sm"><span class="font-bold">Email:</span> {{ cliente?.email }}</p>
            <p class="text-sm"><span class="font-bold">Teléfono:</span> {{ cliente?.telefono }}</p>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-700 mb-2">Totales</h3>
            <p class="text-sm"><span class="font-bold">Subtotal:</span> ${{ cotizacion.subtotal.toFixed(2) }}</p>
            <p class="text-sm"><span class="font-bold">Impuesto (7%):</span> ${{ cotizacion.impuesto.toFixed(2) }}</p>
            <p class="text-sm font-bold"><span class="font-bold">Total:</span> ${{ cotizacion.total.toFixed(2) }}</p>
          </div>
        </div>

        <!-- Ítems -->
        <div class="mb-6">
          <h3 class="text-lg font-bold text-gray-700 mb-2">Ítems</h3>
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
        <div v-if="cotizacion.notas" class="mb-6">
          <h3 class="text-lg font-bold text-gray-700 mb-2">Notas</h3>
          <p class="text-sm whitespace-pre-line">{{ cotizacion.notas }}</p>
        </div>

        <!-- Botones inferiores -->
        <div class="flex justify-between items-center mt-6">
          <button
            @click="$router.go(-1)"
            class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Volver
          </button>
          <button
            v-if="cotizacion.estado === 'pendiente'"
            @click="$router.push(`/cotizaciones/${cotizacion.id}/editar`)"
            class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Editar
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <p class="text-red-500">La cotización no existe o no se pudo cargar.</p>
      <button
        @click="$router.push('/cotizaciones')"
        class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Volver a cotizaciones
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { cotizacionesService, clientesService, facturasService } from '../../services/api';

// Router y Route
const router = useRouter();
const route = useRoute();
const toast = useToast();

// Estado
const cotizacion = ref(null);
const cliente = ref(null);
const cargando = ref(true);
const tieneFactura = ref(false);

// Computed
const estadoTexto = computed(() => {
  if (!cotizacion.value) return '';
  
  const estados = {
    'pendiente': 'Pendiente',
    'aprobada': 'Aprobada',
    'rechazada': 'Rechazada'
  };
  
  return estados[cotizacion.value.estado] || cotizacion.value.estado;
});

// Métodos
const cargarCotizacion = async () => {
  try {
    cargando.value = true;
    
    // Cargar cotización
    const cotizacionData = await cotizacionesService.getById(route.params.id);
    cotizacion.value = cotizacionData;
    
    // Cargar cliente
    const clienteData = await clientesService.getById(cotizacion.value.cliente_id);
    cliente.value = clienteData;
    
    // Verificar si ya tiene factura
    if (cotizacion.value.factura) {
      tieneFactura.value = true;
    }
  } catch (error) {
    toast.error('Error al cargar los datos de la cotización');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

const formatearFecha = (fechaStr) => {
  const fecha = new Date(fechaStr);
  return fecha.toLocaleDateString();
};

const cambiarEstado = async (nuevoEstado) => {
  try {
    // Crear objeto con el nuevo estado
    const datos = { 
      estado: nuevoEstado 
    };
    
    await cotizacionesService.update(cotizacion.value.id, datos);
    
    // Actualizar el estado localmente
    cotizacion.value.estado = nuevoEstado;
    
    toast.success(`Cotización ${nuevoEstado === 'aprobada' ? 'aprobada' : 'rechazada'} con éxito`);
    
    // Si se aprueba, verificar si necesitamos habilitar el botón de crear factura
    if (nuevoEstado === 'aprobada') {
      tieneFactura.value = false;
    }
  } catch (error) {
    let mensaje = 'Error al cambiar el estado de la cotización';
    if (error.response && error.response.data && error.response.data.detail) {
      mensaje += ': ' + error.response.data.detail;
    }
    toast.error(mensaje);
    console.error(error);
  }
};

// Actualizar el método generarPDF
const generarPDF = () => {
  // Utilizar la función del servicio para obtener la URL
  const pdfUrl = cotizacionesService.getPdfUrl(cotizacion.value.id);
  window.open(pdfUrl, '_blank');
};

// Actualizar el método crearFactura
const crearFactura = () => {
  router.push({
    name: 'factura-nueva',
    query: { cotizacion_id: cotizacion.value.id }
  });
};
</script>