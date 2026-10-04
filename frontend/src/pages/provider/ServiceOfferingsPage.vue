<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import {
  activateProviderServiceOffering,
  deactivateProviderServiceOffering,
  listProviderServiceOfferings,
  type ProviderServiceOffering,
} from "../../api/providerServiceOfferings";

import ServiceOfferingStatusBadge from
  "../../components/provider/service-offerings/ServiceOfferingStatusBadge.vue";

const router = useRouter();

const offerings = ref<ProviderServiceOffering[]>([]);

const loading = ref(true);
const error = ref<string | null>(null);
const actionId = ref<string | null>(null);

const page = ref(1);
const pageSize = ref(20);
const total = ref(0);
const totalPages = ref(1);

async function loadOfferings() {
  loading.value = true;
  error.value = null;

  try {
    const response = await listProviderServiceOfferings(
      page.value,
      pageSize.value,
    );

    offerings.value = response.items;
    total.value = response.total;
    totalPages.value = response.total_pages;
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "Failed to load service offerings.";
  } finally {
    loading.value = false;
  }
}

function createOffering() {
  router.push({
    name: "provider-service-offering-create",
  });
}

function editOffering(id: string) {
  router.push({
    name: "provider-service-offering-edit",
    params: { id },
  });
}

async function toggleOffering(
  offering: ProviderServiceOffering,
) {
  actionId.value = offering.id;

  try {
    if (offering.is_active) {
      await deactivateProviderServiceOffering(offering.id);
    } else {
      await activateProviderServiceOffering(offering.id);
    }

    await loadOfferings();
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "Failed to update service offering.";
  } finally {
    actionId.value = null;
  }
}

function previousPage() {
  if (page.value > 1) {
    page.value--;
    loadOfferings();
  }
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++;
    loadOfferings();
  }
}

onMounted(loadOfferings);
</script>

<template>
  <section class="space-y-6">

    <!-- Header -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-[var(--text-primary)]">
          Service Offerings
        </h1>

        <p class="mt-1 text-sm text-[var(--text-secondary)]">
          Configure the services your organization provides.
        </p>
      </div>

      <button
        type="button"
        class="rounded-lg bg-[var(--primary)] px-4 py-2.5 text-sm font-medium text-white transition hover:opacity-90"
        @click="createOffering"
      >
        Add service offering
      </button>
    </div>

    <!-- Error -->
    <div
      v-if="error"
      class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
    >
      {{ error }}
    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-8 text-center text-sm text-[var(--text-secondary)]"
    >
      Loading service offerings...
    </div>

    <!-- Empty -->
    <div
      v-else-if="offerings.length === 0"
      class="rounded-xl border border-dashed border-[var(--border)] bg-[var(--surface)] p-10 text-center"
    >
      <h2 class="text-lg font-medium text-[var(--text-primary)]">
        No service offerings yet
      </h2>

      <p class="mx-auto mt-2 max-w-md text-sm text-[var(--text-secondary)]">
        Select a service from the ServiceHub catalog and configure
        how your organization provides it.
      </p>

      <button
        type="button"
        class="mt-5 rounded-lg bg-[var(--primary)] px-4 py-2.5 text-sm font-medium text-white"
        @click="createOffering"
      >
        Add your first service
      </button>
    </div>

    <!-- Table -->
    <div
      v-else
      class="overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--surface)]"
    >
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-[var(--border)]">
          <thead class="bg-[var(--background)]">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide">
                Service
              </th>

              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide">
                Price
              </th>

              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide">
                Duration
              </th>

              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide">
                Modes
              </th>

              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide">
                Status
              </th>

              <th class="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wide">
                Actions
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-[var(--border)]">
            <tr
              v-for="offering in offerings"
              :key="offering.id"
              class="transition hover:bg-[var(--background)]"
            >
              <td class="px-6 py-4">
                <div class="font-medium text-[var(--text-primary)]">
                  {{ offering.service.name }}
                </div>

                <div class="mt-1 text-xs text-[var(--text-secondary)]">
                  {{ offering.service.slug }}
                </div>
              </td>

              <td class="px-6 py-4 text-sm">
                {{ offering.currency }}
                {{ offering.price }}
              </td>

              <td class="px-6 py-4 text-sm">
                {{ offering.duration_minutes }} min

                <span
                  v-if="offering.buffer_minutes"
                  class="text-xs text-[var(--text-secondary)]"
                >
                  + {{ offering.buffer_minutes }} buffer
                </span>
              </td>

              <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="mode in offering.service_modes"
                    :key="mode"
                    class="rounded-md border border-[var(--border)] px-2 py-1 text-xs"
                  >
                    {{ mode }}
                  </span>
                </div>
              </td>

              <td class="px-6 py-4">
                <ServiceOfferingStatusBadge
                  :active="offering.is_active"
                />
              </td>

              <td class="px-6 py-4">
                <div class="flex justify-end gap-2">
                  <button
                    type="button"
                    class="rounded-md border border-[var(--border)] px-3 py-1.5 text-sm"
                    @click="editOffering(offering.id)"
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    class="rounded-md border border-[var(--border)] px-3 py-1.5 text-sm"
                    :disabled="actionId === offering.id"
                    @click="toggleOffering(offering)"
                  >
                    {{
                      actionId === offering.id
                        ? "Saving..."
                        : offering.is_active
                          ? "Deactivate"
                          : "Activate"
                    }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div
        class="flex items-center justify-between border-t border-[var(--border)] px-6 py-4"
      >
        <p class="text-sm text-[var(--text-secondary)]">
          {{ total }} offering{{ total === 1 ? "" : "s" }}
        </p>

        <div class="flex items-center gap-2">
          <button
            type="button"
            class="rounded-md border border-[var(--border)] px-3 py-1.5 text-sm disabled:opacity-50"
            :disabled="page <= 1"
            @click="previousPage"
          >
            Previous
          </button>

          <span class="px-2 text-sm text-[var(--text-secondary)]">
            {{ page }} / {{ totalPages }}
          </span>

          <button
            type="button"
            class="rounded-md border border-[var(--border)] px-3 py-1.5 text-sm disabled:opacity-50"
            :disabled="page >= totalPages"
            @click="nextPage"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </section>
</template>