<script setup lang="ts">
import { computed, ref } from "vue";

import {
  activateProviderServiceOffering,
  deactivateProviderServiceOffering,
  type ProviderServiceOffering,
} from "../../../api/providerServiceOfferings";

import type { Service } from "../../../api/serviceCatalog";

const props = defineProps<{
  offerings: ProviderServiceOffering[];
  services: Service[];
}>();

const emit = defineEmits<{
  edit: [offering: ProviderServiceOffering];
  changed: [];
}>();

const processingId = ref<string | null>(null);

const serviceMap = computed(() => {
  return new Map(
    props.services.map((service) => [
      service.id,
      service,
    ]),
  );
});

function serviceName(serviceId: string) {
  return (
    serviceMap.value.get(serviceId)?.name ??
    "Unknown service"
  );
}

function formatModes(
  modes: string[],
) {
  return modes
    .map((mode) =>
      mode
        .replaceAll("_", " ")
        .toLowerCase()
        .replace(/\b\w/g, (letter) =>
          letter.toUpperCase(),
        ),
    )
    .join(" · ");
}

async function toggleOffering(
  offering: ProviderServiceOffering,
) {
  processingId.value = offering.id;

  try {
    if (offering.is_active) {
      await deactivateProviderServiceOffering(
        offering.id,
      );
    } else {
      await activateProviderServiceOffering(
        offering.id,
      );
    }

    emit("changed");
  } catch (error) {
    console.error(error);
  } finally {
    processingId.value = null;
  }
}
</script>

<template>
  <div
    v-if="offerings.length === 0"
    class="py-16 text-center"
  >
    <p
      class="font-medium text-[var(--text-primary)]"
    >
      You haven't added any services yet.
    </p>

    <p
      class="mt-1 text-sm text-[var(--text-secondary)]"
    >
      Add a catalog service to start offering it to customers.
    </p>
  </div>

  <div v-else class="space-y-3">
    <article
      v-for="offering in offerings"
      :key="offering.id"
      class="rounded-xl border border-[var(--border-subtle)] p-5"
    >
      <div
        class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"
      >
        <div class="min-w-0">
          <div
            class="flex flex-wrap items-center gap-2"
          >
            <h3
              class="font-semibold text-[var(--text-primary)]"
            >
              {{ serviceName(offering.service_id) }}
            </h3>

            <span
              class="status-badge"
              :class="
                offering.is_active
                  ? 'status-active'
                  : 'status-inactive'
              "
            >
              {{
                offering.is_active
                  ? "Active"
                  : "Inactive"
              }}
            </span>
          </div>

          <div
            class="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-[var(--text-secondary)]"
          >
            <span>
              {{ offering.currency }}
              {{ offering.price }}
            </span>

            <span>
              {{ offering.duration_minutes }} min
            </span>

            <span>
              {{ formatModes(offering.service_modes) }}
            </span>
          </div>

          <p
            v-if="offering.buffer_minutes"
            class="mt-1 text-xs text-[var(--text-secondary)]"
          >
            {{ offering.buffer_minutes }} min buffer
          </p>
        </div>

        <div class="flex flex-wrap gap-2">
          <button
            type="button"
            class="btn-secondary"
            @click="emit('edit', offering)"
          >
            Edit
          </button>

          <button
            type="button"
            class="btn-secondary"
            :disabled="
              processingId === offering.id
            "
            @click="toggleOffering(offering)"
          >
            {{
              processingId === offering.id
                ? "Saving..."
                : offering.is_active
                  ? "Deactivate"
                  : "Activate"
            }}
          </button>
        </div>
      </div>
    </article>
  </div>
</template>