import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import './assets/css/main.css';

// Configuración de toasts
const toastOptions = {
  transition: 'Vue-Toastification__bounce',
  maxToasts: 3,
  newestOnTop: true,
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  showCloseButtonOnHover: false,
};

// Crear la aplicación Vue
const app = createApp(App);

// Registrar plugins
app.use(router);
app.use(Toast, toastOptions);

// Montar la aplicación
app.mount('#app');