import { defineStore } from "pinia";
import { ref } from "vue";

import {
  createProvider,
  getMyProvider,
  updateMyProvider,
} from "../api/providers";

import type {
  Provider,
  ProviderCreateRequest,
  ProviderUpdateRequest,
} from "../types/provider";

export const useProviderStore = defineStore("provider", () => {
  const provider = ref<Provider | null>(null);
  const loading = ref(false);
  const creating = ref(false);
  const updating = ref(false);
  const error = ref<string | null>(null);

  async function fetchProvider() {
    loading.value = true;
    error.value = null;

    try {
      provider.value = await getMyProvider();
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to load provider profile.";

      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function becomeProvider(
    payload: ProviderCreateRequest,
  ) {
    creating.value = true;
    error.value = null;

    try {
      provider.value = await createProvider(payload);

      return provider.value;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to create provider profile.";

      throw err;
    } finally {
      creating.value = false;
    }
  }

  async function updateProvider(
    payload: ProviderUpdateRequest,
  ) {
    updating.value = true;
    error.value = null;

    try {
      provider.value = await updateMyProvider(payload);

      return provider.value;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to update provider profile.";

      throw err;
    } finally {
      updating.value = false;
    }
  }

  function clearProvider() {
    provider.value = null;
    error.value = null;
  }

  return {
    provider,
    loading,
    creating,
    updating,
    error,
    fetchProvider,
    becomeProvider,
    updateProvider,
    clearProvider,
  };
});