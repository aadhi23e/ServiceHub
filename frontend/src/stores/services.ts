import { defineStore } from "pinia";
import { ref } from "vue";

import {
  activateService,
  createService,
  deactivateService,
  getMyService,
  getMyServices,
  updateService,
} from "../api/services";

import type {
  Service,
  ServiceCreateRequest,
  ServiceUpdateRequest,
} from "../types/service";

export const useServicesStore = defineStore("services", () => {
  const services = ref<Service[]>([]);
  const selectedService = ref<Service | null>(null);

  const total = ref(0);
  const offset = ref(0);
  const limit = ref(50);

  const loading = ref(false);
  const saving = ref(false);
  const error = ref<string | null>(null);

  async function fetchServices(
    requestedOffset = 0,
    requestedLimit = 50,
  ) {
    loading.value = true;
    error.value = null;

    try {
      const response = await getMyServices(
        requestedOffset,
        requestedLimit,
      );

      services.value = response.items;
      total.value = response.total;
      offset.value = response.offset;
      limit.value = response.limit;

      return response;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to load services.";

      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchService(serviceId: number) {
    loading.value = true;
    error.value = null;

    try {
      selectedService.value = await getMyService(serviceId);

      return selectedService.value;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to load service.";

      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function addService(
    payload: ServiceCreateRequest,
  ) {
    saving.value = true;
    error.value = null;

    try {
      const service = await createService(payload);

      services.value = [service, ...services.value];
      total.value += 1;

      return service;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to create service.";

      throw err;
    } finally {
      saving.value = false;
    }
  }

  async function editService(
    serviceId: number,
    payload: ServiceUpdateRequest,
  ) {
    saving.value = true;
    error.value = null;

    try {
      const service = await updateService(
        serviceId,
        payload,
      );

      const index = services.value.findIndex(
        (item) => item.id === service.id,
      );

      if (index !== -1) {
        services.value[index] = service;
      }

      if (selectedService.value?.id === service.id) {
        selectedService.value = service;
      }

      return service;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to update service.";

      throw err;
    } finally {
      saving.value = false;
    }
  }

  async function activate(serviceId: number) {
    saving.value = true;
    error.value = null;

    try {
      const service = await activateService(serviceId);
      replaceService(service);

      return service;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to activate service.";

      throw err;
    } finally {
      saving.value = false;
    }
  }

  async function deactivate(serviceId: number) {
    saving.value = true;
    error.value = null;

    try {
      const service = await deactivateService(serviceId);
      replaceService(service);

      return service;
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Failed to deactivate service.";

      throw err;
    } finally {
      saving.value = false;
    }
  }

  function replaceService(service: Service) {
    const index = services.value.findIndex(
      (item) => item.id === service.id,
    );

    if (index !== -1) {
      services.value[index] = service;
    }

    if (selectedService.value?.id === service.id) {
      selectedService.value = service;
    }
  }

  function clear() {
    services.value = [];
    selectedService.value = null;
    total.value = 0;
    error.value = null;
  }

  return {
    services,
    selectedService,
    total,
    offset,
    limit,
    loading,
    saving,
    error,
    fetchServices,
    fetchService,
    addService,
    editService,
    activate,
    deactivate,
    clear,
  };
});