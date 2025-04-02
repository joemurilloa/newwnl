<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Clientes</h1>
      <router-link
        to="/clientes/nuevo"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Nuevo Cliente
      </router-link>
    </div>

    <!-- Buscador -->
    <div class="mb-6">
      <div class="relative">
        <input
          v-model="terminoBusqueda"
          @input="buscarClientes"
          type="text"
          placeholder="Buscar por nombre, apellido o email..."
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button 
          v-if="terminoBusqueda" 
          @click="limpiarBusqueda"
          class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- Lista de clientes -->
    <div v-if="cargando" class="text-center py-8">
      <p class="text-gray-600">Cargando clientes...</p>
    </div>

    <div v-else-if="clientes.length === 0" class="text-center py-8">
      <p v-if="terminoBusqueda" class="text-gray-600">
        No se encontraron clientes que coincidan con "{{ terminoBusqueda }}".
      </p>
      <p v-else class="text-gray-600">
        No hay clientes registrados. ¡Agrega tu primer cliente!
      </p>
    </div>

    <div v-else class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full">
        <thead class="bg-gray-100">
          <tr>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Nombre
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Teléfono
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="cliente in clientes" :key="cliente.id" class="hover:bg-gray-50">
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ cliente.nombre }} {{ cliente.apellido }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">{{ cliente.email }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">{{ cliente.telefono }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap text-sm font-medium">
              <div class="flex space-x-2">
                <router-link
                  :to="`/clientes/${cliente.id}`"
                  class="text-indigo-600 hover:text-indigo-900"
                >
                  Ver
                </router-link>
                <router-link
                  :to="`/clientes/${cliente.id}/editar`"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Editar
                </router-link>
                <button
                  @click="confirmarEliminar(cliente)"
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

    <!-- Modal de confirmación -->
    <div v-if="mostrarModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-bold text-gray-900 mb-4">Confirmar eliminación</h3>
        <p class="text-gray-600 mb-6">
          ¿Estás seguro de que deseas eliminar al cliente {{ clienteAEliminar?.nombre }} {{ clienteAEliminar?.apellido }}? Esta acción no se puede deshacer.
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="cancelarEliminar"
            class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Cancelar
          </button>
          <button
            @click="eliminarCliente"
            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { clientesService } from '../../services/api';

// Toast
const toast = useToast();

// Estado
const clientes = ref([]);
const cargando = ref(true);
const terminoBusqueda = ref('');
const mostrarModal = ref(false);
const clienteAEliminar = ref(null);

// Métodos
const cargarClientes = async () => {
  try {
    cargando.value = true;
    const data = await clientesService.getAll();
    clientes.value = data;
  } catch (error) {
    toast.error('Error al cargar los clientes');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

const buscarClientes = async () => {
  if (!terminoBusqueda.value.trim()) {
    cargarClientes();
    return;
  }
  
  try {
    cargando.value = true;
    const data = await clientesService.buscar(terminoBusqueda.value);
    clientes.value = data;
  } catch (error) {
    toast.error('Error al buscar clientes');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

const limpiarBusqueda = () => {
  terminoBusqueda.value = '';
  cargarClientes();
};

const confirmarEliminar = (cliente) => {
  clienteAEliminar.value = cliente;
  mostrarModal.value = true;
};

const cancelarEliminar = () => {
  clienteAEliminar.value = null;
  mostrarModal.value = false;
};

const eliminarCliente = async () => {
  if (!clienteAEliminar.value) return;
  
  try {
    await clientesService.delete(clienteAEliminar.value.id);
    toast.success('Cliente eliminado con éxito');
    
    // Actualizar la lista
    clientes.value = clientes.value.filter(c => c.id !== clienteAEliminar.value.id);
    
    // Cerrar modal
    cancelarEliminar();
  } catch (error) {
    toast.error('Error al eliminar el cliente');
    console.error(error);
  }
};

// Ciclo de vida
onMounted(() => {
  cargarClientes();
});
</script>