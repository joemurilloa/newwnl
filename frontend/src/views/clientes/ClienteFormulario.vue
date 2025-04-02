<template>
  <div>
    <div class="py-4 px-2">
      <h1 class="text-2xl font-bold text-gray-800 mb-4">
        {{ esEdicion ? 'Editar Cliente' : 'Nuevo Cliente' }}
      </h1>

      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <form @submit.prevent="guardarCliente">
          <!-- Nombre y Apellido -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="nombre" class="block text-gray-700 text-sm font-bold mb-2">
                Nombre
              </label>
              <input
                id="nombre"
                v-model="cliente.nombre"
                type="text"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>
            <div>
              <label for="apellido" class="block text-gray-700 text-sm font-bold mb-2">
                Apellido
              </label>
              <input
                id="apellido"
                v-model="cliente.apellido"
                type="text"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>
          </div>

          <!-- Teléfono y Email -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="telefono" class="block text-gray-700 text-sm font-bold mb-2">
                Teléfono
              </label>
              <input
                id="telefono"
                v-model="cliente.telefono"
                type="text"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>
            <div>
              <label for="email" class="block text-gray-700 text-sm font-bold mb-2">
                Email
              </label>
              <input
                id="email"
                v-model="cliente.email"
                type="email"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>
          </div>

          <!-- Dirección -->
          <div class="mb-6">
            <label for="direccion" class="block text-gray-700 text-sm font-bold mb-2">
              Dirección
            </label>
            <textarea
              id="direccion"
              v-model="cliente.direccion"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              rows="3"
              required
            ></textarea>
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
              :disabled="cargando"
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
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { clientesService } from '../../services/api';

// Router y Route
const router = useRouter();
const route = useRoute();
const toast = useToast();

// Estado
const cliente = ref({
  nombre: '',
  apellido: '',
  telefono: '',
  email: '',
  direccion: '',
});
const cargando = ref(false);
const esEdicion = computed(() => !!route.params.id);

// Métodos
const cargarCliente = async () => {
  if (esEdicion.value) {
    try {
      cargando.value = true;
      const clienteData = await clientesService.getById(route.params.id);
      cliente.value = clienteData;
    } catch (error) {
      toast.error('Error al cargar los datos del cliente');
      console.error(error);
    } finally {
      cargando.value = false;
    }
  }
};

const guardarCliente = async () => {
  try {
    cargando.value = true;
    
    if (esEdicion.value) {
      await clientesService.update(route.params.id, cliente.value);
      toast.success('Cliente actualizado con éxito');
    } else {
      await clientesService.create(cliente.value);
      toast.success('Cliente creado con éxito');
    }
    
    router.push('/clientes');
  } catch (error) {
    toast.error('Error al guardar el cliente');
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

// Ciclo de vida
onMounted(() => {
  cargarCliente();
});
</script>