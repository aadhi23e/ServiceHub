<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import {
  listServices,
  type Service,
  type ServiceCategory,
} from "../../api/serviceCatalog";

import {
  listProviderServiceOfferings,
  type ProviderServiceOffering,
} from "../../api/providerServiceOfferings";

import ProviderServiceOfferingForm from "../../components/provider/service-offerings/ProviderServiceOfferingForm.vue";
import ProviderServiceOfferingList from "../../components/provider/service-offerings/ProviderServiceOfferingList.vue";

const services = ref<Service[]>([]);
const offerings = ref<ProviderServiceOffering[]>([]);

const loading = ref(true);
const errorMessage = ref("");

const showForm = ref(false);
const editingOffering = ref<ProviderServiceOffering | null>(null);

const availableServices = computed(() => {
  const offeredServiceIds = new Set(
    offerings.value.map(
      (offering) => offering.service_id,
    ),
  );

  return services.value.filter(
    (service) =>
      service.is_active &&
      !offeredServiceIds.has(service.id),
  );
});

async function loadPage() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const [serviceData, offeringData] =
      await Promise.all([
        listServices(),
        listProviderServiceOfferings(),
      ]);

    services.value = serviceData;
    offerings.value = offeringData;
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Unable to load provider services.";
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  editingOffering.value = null;
  showForm.value = true;
}

function openEdit(
  offering: ProviderServiceOffering,
) {
  editingOffering.value = offering;
  showForm.value = true;
}

function closeForm() {
  showForm.value = false;
  editingOffering.value = null;
}

async function handleSaved() {
  closeForm();
  await loadPage();
}

onMounted(loadPage);
</script>

<template>
  <div class="space-y-6">
    <section
      class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"
    >
      <div>
        <p class="page-eyebrow">Provider</p>

        <h1 class="page-title">
          My Services
        </h1>

        <p class="page-description">
          Choose services from the ServiceHub catalog
          and configure how your organization offers them.
        </p>
      </div>

      <button
        type="button"
        class="btn-primary"
        :disabled="availableServices.length === 0"
        @click="openCreate"
      >
        <span>+</span>
        Add service
      </button>
    </section>

    <div
      v-if="errorMessage"
      class="alert-error"
      role="alert"
    >
      <div>
        <p class="font-semibold">
          Unable to load services
        </p>

        <p class="mt-1 text-sm">
          {{ errorMessage }}
        </p>
      </div>

      <button
        type="button"
        class="btn-secondary"
        @click="loadPage"
      >
        Retry
      </button>
    </div>

    <section class="grid gap-4 sm:grid-cols-3">
      <article class="surface-card p-5">
        <p class="metric-label">
          Total services
        </p>

        <p class="metric-value">
          {{ offerings.length }}
        </p>
      </article>

      <article class="surface-card p-5">
        <p class="metric-label">
          Active services
        </p>

        <p class="metric-value">
          {{
            offerings.filter(
              (offering) => offering.is_active,
            ).length
          }}
        </p>
      </article>

      <article class="surface-card p-5">
        <p class="metric-label">
          Available catalog services
        </p>

        <p class="metric-value">
          {{ availableServices.length }}
        </p>
      </article>
    </section>

    <section class="surface-card overflow-hidden">
      <div
        class="border-b border-[var(--border-subtle)] px-4 py-4 sm:px-6"
      >
        <h2 class="text-base font-semibold text-[var(--text-primary)]">
          Services offered by your organization
        </h2>
      </div>

      <div class="p-4 sm:p-6">
        <div
          v-if="loading"
          class="py-16 text-center"
        >
          <div class="loading-spinner mx-auto" />

          <p
            class="mt-4 text-sm text-[var(--text-secondary)]"
          >
            Loading your services...
          </p>
        </div>

        <ProviderServiceOfferingList
          v-else
          :offerings="offerings"
          :services="services"
          @edit="openEdit"
          @changed="loadPage"
        />
      </div>
    </section>

    <ProviderServiceOfferingForm
      v-if="showForm"
      :offering="editingOffering"
      :services="availableServices"
      @close="closeForm"
      @saved="handleSaved"
    />
  </div>
</template>