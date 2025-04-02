import axios from 'axios';

// Configuración de Axios con mejor manejo de errores
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos
});

// Interceptor para mostrar errores detallados en la consola
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('Error en la petición API:');
    if (error.response) {
      // El servidor respondió con un código de error
      console.error('Datos:', error.response.data);
      console.error('Código de estado:', error.response.status);
    } else if (error.request) {
      // La petición se hizo pero no hubo respuesta
      console.error('No se recibió respuesta del servidor');
    } else {
      // Error al configurar la petición
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Servicios para Clientes
export const clientesService = {
  // Obtener todos los clientes
  getAll: async () => {
    try {
      const response = await apiClient.get('/clientes/');
      return response.data;
    } catch (error) {
      console.error('Error específico en getAll clientes:', error.message);
      throw error;
    }
  },
  
  // Obtener un cliente por ID
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/clientes/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al obtener cliente ${id}:`, error.message);
      throw error;
    }
  },
  
  // Crear un nuevo cliente
  create: async (cliente) => {
    try {
      const response = await apiClient.post('/clientes/', cliente);
      return response.data;
    } catch (error) {
      console.error('Error al crear cliente:', error.message);
      throw error;
    }
  },
  
  // Actualizar un cliente
  update: async (id, cliente) => {
    try {
      const response = await apiClient.put(`/clientes/${id}`, cliente);
      return response.data;
    } catch (error) {
      console.error(`Error al actualizar cliente ${id}:`, error.message);
      throw error;
    }
  },
  
  // Eliminar un cliente
  delete: async (id) => {
    try {
      await apiClient.delete(`/clientes/${id}`);
    } catch (error) {
      console.error(`Error al eliminar cliente ${id}:`, error.message);
      throw error;
    }
  },
  
  // Buscar clientes
  buscar: async (termino) => {
    try {
      const response = await apiClient.get(`/clientes/buscar/?termino=${termino}`);
      return response.data;
    } catch (error) {
      console.error(`Error al buscar clientes con término "${termino}":`, error.message);
      throw error;
    }
  },
};

// Servicios para Cotizaciones
export const cotizacionesService = {
  // Implementación similar con mejor manejo de errores...
  getAll: async () => {
    try {
      const response = await apiClient.get('/cotizaciones/');
      return response.data;
    } catch (error) {
      console.error('Error al obtener cotizaciones:', error.message);
      throw error;
    }
  },
  
  // Resto de métodos...
};

// Servicios para Facturas
export const facturasService = {
  // Implementación similar con mejor manejo de errores...
  getAll: async () => {
    try {
      const response = await apiClient.get('/facturas/');
      return response.data;
    } catch (error) {
      console.error('Error al obtener facturas:', error.message);
      throw error;
    }
  },
  
  // Resto de métodos...
};

export default {
  clientes: clientesService,
  cotizaciones: cotizacionesService,
  facturas: facturasService,
};