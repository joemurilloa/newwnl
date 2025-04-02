import { createRouter, createWebHistory } from 'vue-router';

// Importar vistas
import Home from '../views/Home.vue';

// Importar vistas de clientes
import ClientesLista from '../views/clientes/ClientesLista.vue';
import ClienteDetalle from '../views/clientes/ClienteDetalle.vue';
import ClienteFormulario from '../views/clientes/ClienteFormulario.vue';

// Importar vistas de cotizaciones
import CotizacionesLista from '../views/cotizaciones/CotizacionesLista.vue';
import CotizacionDetalle from '../views/cotizaciones/CotizacionDetalle.vue';
import CotizacionFormulario from '../views/cotizaciones/CotizacionFormulario.vue';

// Importar vistas de facturas
import FacturasLista from '../views/facturas/FacturasLista.vue';
import FacturaDetalle from '../views/facturas/FacturaDetalle.vue';
import FacturaFormulario from '../views/facturas/FacturaFormulario.vue';

// Definir rutas
const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  // Rutas de clientes
  {
    path: '/clientes',
    name: 'clientes',
    component: ClientesLista,
  },
  {
    path: '/clientes/nuevo',
    name: 'cliente-nuevo',
    component: ClienteFormulario,
  },
  {
    path: '/clientes/:id',
    name: 'cliente-detalle',
    component: ClienteDetalle,
    props: true,
  },
  {
    path: '/clientes/:id/editar',
    name: 'cliente-editar',
    component: ClienteFormulario,
    props: true,
  },
  // Rutas de cotizaciones
  {
    path: '/cotizaciones',
    name: 'cotizaciones',
    component: CotizacionesLista,
  },
  {
    path: '/cotizaciones/nueva',
    name: 'cotizacion-nueva',
    component: CotizacionFormulario,
  },
  {
    path: '/cotizaciones/:id',
    name: 'cotizacion-detalle',
    component: CotizacionDetalle,
    props: true,
  },
  {
    path: '/cotizaciones/:id/editar',
    name: 'cotizacion-editar',
    component: CotizacionFormulario,
    props: true,
  },
  // Rutas de facturas
  {
    path: '/facturas',
    name: 'facturas',
    component: FacturasLista,
  },
  {
    path: '/facturas/nueva',
    name: 'factura-nueva',
    component: FacturaFormulario,
  },
  {
    path: '/facturas/:id',
    name: 'factura-detalle',
    component: FacturaDetalle,
    props: true,
  },
  // Ruta para manejar páginas no encontradas
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFound.vue'),
  },
];

// Crear router
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    // Volver al inicio de la página en cada navegación
    return { top: 0 };
  },
});

export default router;