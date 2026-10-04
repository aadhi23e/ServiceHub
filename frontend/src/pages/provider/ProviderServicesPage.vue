<script setup lang="ts">
import { onMounted, ref } from 'vue';

import {
  providerServiceOfferingsApi,
} from '../../api/providerServiceOfferings';

import {
  useProviderRole,
} from '../../composables/provider/useProviderRole';

import ServiceOfferingCard from '../../components/provider/ServiceOfferingCard.vue';

import type {
  ProviderServiceOffering,
} from '../../types/provider';

const {
  canManageServices,
} = useProviderRole();

const offerings =
  ref<ProviderServiceOffering[]>([]);

const loading = ref(true);
const error = ref<string | null>(null);

async function loadOfferings() {
  loading.value = true;
  error.value = null;

  try {
    const response =
      await providerServiceOfferingsApi.list();

    offerings.value = response.items;
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to load services.';
  } finally {
    loading.value = false;
  }
}

async function activate(
  offeringId: string,
) {
  try {
    const updated =
      await providerServiceOfferingsApi.activate(
        offeringId,
      );

    replaceOffering(updated);
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to activate service.';
  }
}

async function deactivate(
  offeringId: string,
) {
  try {
    const updated =
      await providerServiceOfferingsApi.deactivate(
        offeringId,
      );

    replaceOffering(updated);
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to deactivate service.';
  }
}

function replaceOffering(
  offering: ProviderServiceOffering,
) {
  const index =
    offerings.value.findIndex(
      item => item.id === offering.id,
    );

  if (index !== -1) {
    offerings.value[index] = offering;
  }
}

onMounted(loadOfferings);
</script>

<template>
  <section class="space-y-6">
    <header
      class="flex items-start justify-between gap-4"
    >
      <div>
        <h1 class="text-2xl font-semibold">
          Services
        </h1>

        <p
          class="mt-1 text-sm text-[var(--text-muted)]"
        >
          Manage the services your organization
          provides.
        </p>
      </div>

      <RouterLink
        v-if="canManageServices"
        to="/services/new"
        class="button-primary"
      >
        Add service
      </RouterLink>
    </header>

    <div
      v-if="loading"
      class="dashboard-card"
    >
      Loading services...
    </div>

    <div
      v-else-if="error"
      class="dashboard-card"
    >
      <p class="text-sm text-[var(--danger)]">
        {{ error }}
      </p>

      <button
        class="button-secondary mt-4"
        @click="loadOfferings"
      >
        Try again
      </button>
    </div>

    <div
      v-else-if="offerings.length === 0"
      class="dashboard-card"
    >
      <h2 class="font-semibold">
        No service offerings
      </h2>

      <p
        class="mt-1 text-sm text-[var(--text-muted)]"
      >
        Your organization has not added any
        services yet.
      </p>

      <RouterLink
        v-if="canManageServices"
        to="/services/new"
        class="button-primary mt-4 inline-flex"
      >
        Add service
      </RouterLink>
    </div>

    <div
      v-else
      class="grid gap-5 lg:grid-cols-2"
    >
      <ServiceOfferingCard
        v-for="offering in offerings"
        :key="offering.id"
        :offering="offering"
        :can-manage="canManageServices"
        @activate="activate"
        @deactivate="deactivate"
      />
    </div>
  </section>
</template>