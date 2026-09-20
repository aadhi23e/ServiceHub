import { createApp } from "vue";
import { pinia } from "./app/pinia";

import App from "./App.vue";
import router from "./router";
import { useThemeStore } from "./stores/theme";

import "./styles/main.css";

const app = createApp(App);

app.use(pinia);
app.use(router);

const themeStore = useThemeStore(pinia);

themeStore.initialize();

app.mount("#app");