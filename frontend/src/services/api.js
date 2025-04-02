import axios from 'axios';

// Configuración de Axios
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos
});

// Servicios para Clientes
export const clientesService = {
  // Obtener todos los clientes
  getAll: async () => {
    const response = await apiClient.get('/clientes/');
    return response.data;
  },
  
  // Obtener un cliente por ID
  getById: async (id) => {
    const response = await apiClient.get(`/clientes/${id}`);
    return response.data;
  },
  
  // Crear un nuevo cliente
  create: async (cliente) => {
    const response = await apiClient.post('/clientes/', cliente);
    return response.data;
  },
  
  // Actualizar un cliente
  update: async (id, cliente) => {
    const response = await apiClient.put(`/clientes/${id}`, cliente);
    return response.data;
  },
  
  // Eliminar un cliente
  delete: async (id) => {
    await apiClient.delete(`/clientes/${id}`);
  },
  
  // Buscar clientes
  buscar: async (termino) => {
    const response = await apiClient.get(`/clientes/buscar/?termino=${termino}`);
    return response.data;
  },
};

// Servicios para Cotizaciones
export const cotizacionesService = {
  // Obtener todas las cotizaciones
  getAll: async () => {
    const response = await apiClient.get('/cotizaciones/');
    return response.data;
  },
  
  // Obtener cotizaciones aprobadas
  getAprobadas: async () => {
    const response = await apiClient.get('/cotizaciones/aprobadas');
    return response.data;
  },
  
  // Obtener una cotización por ID
  getById: async (id) => {
    const response = await apiClient.get(`/cotizaciones/${id}`);
    return response.data;
  },
  
  // Crear una nueva cotización
  create: async (cotizacion) => {
    const response = await apiClient.post('/cotizaciones/', cotizacion);
    return response.data;
  },
  
  // Actualizar una cotización
  update: async (id, cotizacion) => {
    const response = await apiClient.put(`/cotizaciones/${id}`, cotizacion);
    return response.data;
  },
  
  // Eliminar una cotización
  delete: async (id) => {
    await apiClient.delete(`/cotizaciones/${id}`);
  },
  
  // Obtener URL del PDF de cotización
  getPdfUrl: (id) => {
    return `http://localhost:8000/api/cotizaciones/${id}/pdf`;
  },
};

// Servicios para Facturas
export const facturasService = {
  // Obtener todas las facturas
  getAll: async () => {
    const response = await apiClient.get('/facturas/');
    return response.data;
  },
  
  // Obtener una factura por ID
  getById: async (id) => {
    const response = await apiClient.get(`/facturas/${id}`);
    return response.data;
  },
  
  // Crear una nueva factura
  create: async (factura) => {
    const response = await apiClient.post('/facturas/', factura);
    return response.data;
  },
  
  // Actualizar una factura
  update: async (id, factura) => {
    const response = await apiClient.put(`/facturas/${id}`, factura);
    return response.data;
  },
  
  // Obtener URL del PDF de factura
  getPdfUrl: (id) => {
    return `http://localhost:8000/api/facturas/${id}/pdf`;
  },
};

export default {
  clientes: clientesService,
  cotizaciones: cotizacionesService,
  facturas: facturasService,
};