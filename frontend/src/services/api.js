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
  // Obtener todas las cotizaciones
  getAll: async () => {
    try {
      const response = await apiClient.get('/cotizaciones/');
      return response.data;
    } catch (error) {
      console.error('Error al obtener cotizaciones:', error.message);
      throw error;
    }
  },
  
  // Obtener cotizaciones aprobadas
  getAprobadas: async () => {
    try {
      const response = await apiClient.get('/cotizaciones/aprobadas');
      return response.data;
    } catch (error) {
      console.error('Error al obtener cotizaciones aprobadas:', error.message);
      throw error;
    }
  },
  
  // Obtener una cotización por ID
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/cotizaciones/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al obtener cotización ${id}:`, error.message);
      throw error;
    }
  },
  
  // Crear una nueva cotización
  create: async (cotizacion) => {
    try {
      const response = await apiClient.post('/cotizaciones/', cotizacion);
      return response.data;
    } catch (error) {
      console.error('Error al crear cotización:', error.message);
      throw error;
    }
  },
  
  // Actualizar una cotización
  update: async (id, cotizacion) => {
    try {
      const response = await apiClient.put(`/cotizaciones/${id}`, cotizacion);
      return response.data;
    } catch (error) {
      console.error(`Error al actualizar cotización ${id}:`, error.message);
      throw error;
    }
  },
  
  // Eliminar una cotización
  delete: async (id) => {
    try {
      await apiClient.delete(`/cotizaciones/${id}`);
    } catch (error) {
      console.error(`Error al eliminar cotización ${id}:`, error.message);
      throw error;
    }
  },
  
  // Obtener URL para PDF de cotización
  getPdfUrl: (id) => {
    return `${apiClient.defaults.baseURL}/cotizaciones/${id}/pdf`;
  }
};

// Servicios para Facturas
export const facturasService = {
  // Obtener todas las facturas
  getAll: async () => {
    try {
      const response = await apiClient.get('/facturas/');
      return response.data;
    } catch (error) {
      console.error('Error al obtener facturas:', error.message);
      throw error;
    }
  },
  
  // Obtener una factura por ID
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/facturas/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error al obtener factura ${id}:`, error.message);
      throw error;
    }
  },
  
  // Crear una nueva factura
  create: async (factura) => {
    try {
      const response = await apiClient.post('/facturas/', factura);
      return response.data;
    } catch (error) {
      console.error('Error al crear factura:', error.message);
      throw error;
    }
  },
  
  // Actualizar una factura
  update: async (id, factura) => {
    try {
      const response = await apiClient.put(`/facturas/${id}`, factura);
      return response.data;
    } catch (error) {
      console.error(`Error al actualizar factura ${id}:`, error.message);
      throw error;
    }
  },
  
  // Obtener URL para PDF de factura
  getPdfUrl: (id) => {
    return `${apiClient.defaults.baseURL}/facturas/${id}/pdf`;
  }
};

export default {
  clientes: clientesService,
  cotizaciones: cotizacionesService,
  facturas: facturasService,
};