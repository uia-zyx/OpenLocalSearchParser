import Aura from '@primevue/themes/aura';
import PrimeVue from 'primevue/config';
import { createPinia } from 'pinia';
import { createApp } from 'vue';

import 'primeicons/primeicons.css';
import '../styles/main.css';
import App from './App.vue';
import { router } from '../router';

createApp(App)
  .use(createPinia())
  .use(router)
  .use(PrimeVue, {
    theme: {
      preset: Aura,
    },
  })
  .mount('#app');

