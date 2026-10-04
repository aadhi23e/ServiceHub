<script setup lang="ts">
import { reactive, ref } from "vue";

import {
  createProviderServiceOffering,
  updateProviderServiceOffering,
  type ProviderServiceOffering,
  type ServiceMode,
} from "../../../api/providerServiceOfferings";

import type { Service } from "../../../api/serviceCatalog";

const props = defineProps<{
  offering: ProviderServiceOffering | null;
  services: Service[];
}>();

const emit = defineEmits<{
  close: [];
  saved: [];
}>();

const editing = Boolean(props.offering);

const form = reactive({
  service_id: props.offering?.service_id ?? "",
  price: props.offering
    ? Number(props.offering.price)
    : 0,
  currency: props.offering?.currency ?? "INR",
  duration_minutes:
    props.offering?.duration_minutes ?? 60,
  buffer_minutes:
    props.offering?.buffer_minutes ?? 0,
  service_modes:
    [...(props.offering?.service_modes ?? [])] as ServiceMode[],
});

const loading = ref(false);
const errorMessage = ref("");

const serviceModeOptions: {
  value: ServiceMode;
  label: string;
}[] = [
  {
    value: "HOME_SERVICE",
    label: "Home service",
  },
  {
    value: "ON_SITE",
    label: "On site",
  },
];

function toggleMode(mode: ServiceMode) {
  if (form.service_modes.includes(mode)) {
    form.service_modes =
      form.service_modes.filter(
        (item) => item !== mode,
      );
  } else {
    form.service_modes.push(mode);
  }
}

async function submit() {
  errorMessage.value = "";

  if (!editing && !form.service_id) {
    errorMessage.value =
      "Please select a service.";

    return;
  }

  if (form.service_modes.length === 0) {
    errorMessage.value =
      "Select at least one service mode.";

    return;
  }

  loading.value = true;

  try {
    if (props.offering) {
      await updateProviderServiceOffering(
        props.offering.id,
        {
          price: form.price,
          currency: form.currency
            .trim()
            .toUpperCase(),
          duration_minutes:
            form.duration_minutes,
          buffer_minutes:
            form.buffer_minutes,
          service_modes:
            form.service_modes,
        },
      );
    } else {
      await createProviderServiceOffering({
        service_id: form.service_id,
        price: form.price,
        currency: form.currency
          .trim()
          .toUpperCase(),
        duration_minutes:
          form.duration_minutes,
        buffer_minutes:
          form.buffer_minutes,
        service_modes:
          form.service_modes,
      });
    }

    emit("saved");
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Unable to save service offering.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="modal-backdrop">
    <div
      class="modal-panel max-w-xl"
      role="dialog"
      aria-modal="true"
    >
      <div
        class="border-b border-[var(--border-subtle)] px-6 py-5"
      >
        <div
          class="flex items-start justify-between gap-4"
        >
          <div>
            <p class="page-eyebrow">
              Provider service
            </p>

            <h2
              class="text-xl font-semibold text-[var(--text-primary)]"
            >
              {{
                editing
                  ? "Edit service"
                  : "Add service"
              }}
            </h2>
          </div>

          <button
            type="button"
            class="btn-icon"
            @click="emit('close')"
          >
            ×
          </button>
        </div>
      </div>

      <form
        class="space-y-5 px-6 py-6"
        @submit.prevent="submit"
      >
        <div v-if="!editing">
          <label class="form-label">
            Service
          </label>

          <select
            v-model="form.service_id"
            class="form-input"
            required
          >
            <option value="" disabled>
              Select a ServiceHub service
            </option>

            <option
              v-for="service in services"
              :key="service.id"
              :value="service.id"
            >
              {{ service.name }}
            </option>
          </select>
        </div>

        <div v-else>
          <label class="form-label">
            Service
          </label>

          <div
            class="rounded-lg border border-[var(--border-subtle)] bg-[var(--surface-muted)] px-4 py-3"
          >
            {{
              services.find(
                (service) =>
                  service.id === form.service_id,
              )?.name ?? "Current service"
            }}
          </div>
        </div>

        <div
          v-if="errorMessage"
          class="alert-error"
          role="alert"
        >
          {{ errorMessage }}
        </div>

        <div class="grid gap-5 sm:grid-cols-2">
          <div>
            <label class="form-label">
              Price
            </label>

            <input
              v-model.number="form.price"
              type="number"
              min="0"
              step="0.01"
              class="form-input"
              required
            />
          </div>

          <div>
            <label class="form-label">
              Currency
            </label>

            <input
              v-model="form.currency"
              type="text"
              maxlength="3"
              class="form-input uppercase"
              required
            />
          </div>
        </div>

        <div class="grid gap-5 sm:grid-cols-2">
          <div>
            <label class="form-label">
              Duration
            </label>

            <div class="relative">
              <input
                v-model.number="form.duration_minutes"
                type="number"
                min="1"
                max="1440"
                class="form-input pr-20"
                required
              />

              <span
                class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-sm text-[var(--text-secondary)]"
              >
                minutes
              </span>
            </div>
          </div>

          <div>
            <label class="form-label">
              Buffer
            </label>

            <div class="relative">
              <input
                v-model.number="form.buffer_minutes"
                type="number"
                min="0"
                max="1440"
                class="form-input pr-20"
              />

              <span
                class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-sm text-[var(--text-secondary)]"
              >
                minutes
              </span>
            </div>
          </div>
        </div>

        <div>
          <label class="form-label">
            Service modes
          </label>

          <div class="space-y-2">
            <label
              v-for="mode in serviceModeOptions"
              :key="mode.value"
              class="flex cursor-pointer items-center gap-3 rounded-lg border border-[var(--border-subtle)] px-4 py-3"
            >
              <input
                type="checkbox"
                :checked="
                  form.service_modes.includes(
                    mode.value,
                  )
                "
                @change="toggleMode(mode.value)"
              />

              <span
                class="text-sm text-[var(--text-primary)]"
              >
                {{ mode.label }}
              </span>
            </label>
          </div>
        </div>

        <div
          class="flex justify-end gap-3 border-t border-[var(--border-subtle)] pt-5"
        >
          <button
            type="button"
            class="btn-secondary"
            :disabled="loading"
            @click="emit('close')"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="btn-primary"
            :disabled="loading"
          >
            {{
              loading
                ? "Saving..."
                : editing
                  ? "Save changes"
                  : "Add service"
            }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>