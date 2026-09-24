import { createApp } from 'vue';

import App from './App.vue';
import router from './router';
import { pinia } from './app/pinia';

import { useThemeStore } from './stores/theme';
import { useAuthStore } from './stores/auth';

import './styles/main.css';

async function bootstrap(): Promise<void> {
  const app = createApp(App);

  app.use(pinia);

  const themeStore = useThemeStore(pinia);
  const authStore = useAuthStore(pinia);

  themeStore.initialize();

  // Restore the authentication session BEFORE
  // Vue Router performs its first navigation.
  await authStore.initialize();

  app.use(router);

  await router.isReady();

  app.mount('#app');
}

bootstrap();
