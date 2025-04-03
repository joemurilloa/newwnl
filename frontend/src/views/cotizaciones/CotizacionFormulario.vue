<template>
  <div>
    <div class="py-4 px-2">
      <h1 class="text-2xl font-bold text-gray-800 mb-4">
        {{ esEdicion ? 'Editar Cotización' : 'Nueva Cotización' }}
      </h1>

      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <form @submit.prevent="guardarCotizacion">
          <!-- Selección de cliente -->
          <div class="mb-4">
            <label for="cliente" class="block text-gray-700 text-sm font-bold mb-2">
              Cliente
            </label>
            <select
              id="cliente"
              v-model="cotizacion.cliente_id"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
              :disabled="esEdicion"
            >
              <option value="" disabled>Seleccione un cliente</option>
              <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                {{ cliente.nombre }} {{ cliente.apellido }}
              </option>
            </select>
          </div>

          <!-- Ítems de la cotización -->
          <div class="mb-4">
            <div class="flex justify-between items-center mb-2">
              <h2 class="text-lg font-bold text-gray-700">Ítems</h2>
              <button
                type="button"
                @click="agregarItem"
                class="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded focus:outline-none focus:shadow-outline text-sm"
              >
                + Agregar Ítem
              </button>
            </div>

            <div v-if="cotizacion.items.length === 0" class="text-gray-500 italic text-center py-4">
              No hay ítems. Haga clic en "Agregar Ítem" para comenzar.
            </div>

            <div v-for="(item, index) in cotizacion.items" :key="index" class="border p-4 mb-3 rounded">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
                <div class="md:col-span-3">
                  <label class="block text-gray-700 text-sm font-bold mb-1">
                    Descripción
                  </label>
                  <input
                    v-model="item.descripcion"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-1">
                    Cantidad
                  </label>
                  <input
                    v-model.number="item.cantidad"
                    type="number"
                    step="0.01"
                    min="0.01"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                    @input="calcularSubtotalItem(index)"
                  />
                </div>
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-1">
                    Unidad
                  </label>
                  <input
                    v-model="item.unidad"
                    type="text"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                  />
                </div>
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-1">
                    Precio Unitario
                  </label>
                  <input
                    v-model.number="item.precio_unitario"
                    type="number"
                    step="0.01"
                    min="0.01"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    required
                    @input="calcularSubtotalItem(index)"
                  />
                </div>
              </div>

              <div class="flex justify-between items-center mt-3">
                <div class="text-gray-700 text-sm font-bold">
                  Subtotal: ${{ calcularSubtotalItem(index).toFixed(2) }}
                </div>
                <button
                  type="button"
                  @click="eliminarItem(index)"
                  class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded focus:outline-none focus:shadow-outline text-sm"
                >
                  Eliminar
                </button>
              </div>
            </div>
          </div>

          <!-- Notas -->
          <div class="mb-6">
            <label for="notas" class="block text-gray-700 text-sm font-bold mb-2">
              Notas
            </label>
            <textarea
              id="notas"
              v-model="cotizacion.notas"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              rows="3"
            ></textarea>
          </div>

          <!-- Totales -->
          <div class="border-t pt-4 mb-6">
            <div class="flex justify-end">
              <div class="w-full md:w-1/3">
                <div class="flex justify-between py-1">
                  <span class="font-bold">Subtotal:</span>
                  <span>${{ calcularSubtotal().toFixed(2) }}</span>
                </div>
                <div class="flex justify-between py-1">
                  <span class="font-bold">Impuesto (7%):</span>
                  <span>${{ calcularImpuesto().toFixed(2) }}</span>
                </div>
                <div class="flex justify-between py-1 text-lg font-bold">
                  <span>Total:</span>
                  <span>${{ calcularTotal().toFixed(2) }}</span>
                </div>
              </div>
            </div>
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
              :disabled="cargando || cotizacion.items.length === 0"
            >
              {{ cargando ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { clientesService, cotizacionesService } from '../../services/api';

// Router y Route
const router = useRouter();
const route = useRoute();
const toast = useToast();

// Estado
const clientes = ref([]);
const cotizacion = ref({
  cliente_id: '',
  items: [],
  notas: '',
});
const cargando = ref(false);
const esEdicion = computed(() => !!route.params.id);

// Métodos
const cargarClientes = async () => {
  try {
    cargando.value = true; // Indicar que está cargando
    const clientesData = await clientesService.getAll();
    clientes.value = clientesData;
  } catch (error) {
    toast.error('Error al cargar los clientes');
    console.error(error);
    clientes.value = []; // Asegurar que sea un array vacío en caso de error
  } finally {
    cargando.value = false; // Desactivar el indicador de carga
  }
};

const cargarCotizacion = async () => {
  if (esEdicion.value) {
    try {
      cargando.value = true;
      const cotizacionData = await cotizacionesService.getById(route.params.id);
      
      // Mapear los items para eliminar propiedades no necesarias
      const items = cotizacionData.items.map(item => ({
        descripcion: item.descripcion,
        cantidad: item.cantidad,
        unidad: item.unidad,
        precio_unitario: item.precio_unitario
      }));
      
      cotizacion.value = {
        cliente_id: cotizacionData.cliente_id,
        items: items,
        notas: cotizacionData.notas
      };
    } catch (error) {
      toast.error('Error al cargar la cotización');
      console.error(error);
    } finally {
      cargando.value = false;
    }
  }
};

const agregarItem = () => {
  cotizacion.value.items.push({
    descripcion: '',
    cantidad: 1,
    unidad: '',
    precio_unitario: 0
  });
};

const eliminarItem = (index) => {
  cotizacion.value.items.splice(index, 1);
};

const calcularSubtotalItem = (index) => {
  const item = cotizacion.value.items[index];
  if (!item.cantidad || !item.precio_unitario) return 0;
  return item.cantidad * item.precio_unitario;
};

const calcularSubtotal = () => {
  return cotizacion.value.items.reduce((total, item, index) => {
    return total + calcularSubtotalItem(index);
  }, 0);
};

const calcularImpuesto = () => {
  return calcularSubtotal() * 0.07; // 7% de impuesto
};

const calcularTotal = () => {
  return calcularSubtotal() + calcularImpuesto();
};

const guardarCotizacion = async () => {
  try {
    cargando.value = true;
    
    // Validar que haya al menos un ítem
    if (cotizacion.value.items.length === 0) {
      toast.error('Debe agregar al menos un ítem a la cotización');
      return;
    }
    
    // Calcular subtotales para cada ítem si no están calculados
    cotizacion.value.items.forEach((item, index) => {
      item.subtotal = calcularSubtotalItem(index);
    });
    
    // Crear objeto de cotización con el formato correcto para el backend
    const cotizacionData = {
      cliente_id: cotizacion.value.cliente_id,
      items: cotizacion.value.items,
      notas: cotizacion.value.notas
    };
    
    if (esEdicion.value) {
      // En edición, el backend espera diferentes campos
      const datosActualizacion = {
        estado: 'pendiente',
        notas: cotizacion.value.notas,
      };
      await cotizacionesService.update(route.params.id, datosActualizacion);
      toast.success('Cotización actualizada con éxito');
    } else {
      await cotizacionesService.create(cotizacionData);
      toast.success('Cotización creada con éxito');
    }
    
    router.push('/cotizaciones');
  } catch (error) {
    toast.error('Error al guardar la cotización: ' + (error.response?.data?.detail || error.message));
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

// Ciclo de vida
onMounted(() => {
  Promise.all([
    esEdicion.value ? cargarCotizacion() : Promise.resolve(),
    cargarClientes()
  ]);
});
</script>