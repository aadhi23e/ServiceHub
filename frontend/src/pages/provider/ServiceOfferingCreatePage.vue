<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import {
  createProviderServiceOffering,
  getProviderServiceOffering,
  updateProviderServiceOffering,
  type ProviderServiceOfferingCreateRequest,
} from "../../api/providerServiceOfferings";

import {
  listServices,
//   type Service,
} from "../../api/services";
import { Service } from "../../types/service"
const route = useRoute();
const router = useRouter();

const offeringId = computed(() =>
  typeof route.params.id === "string"
    ? route.params.id
    : null,
);

const isEdit = computed(() => Boolean(offeringId.value));

const services = ref<Service[]>([]);

const loading = ref(true);
const saving = ref(false);
const error = ref<string | null>(null);

const form = ref<ProviderServiceOfferingCreateRequest>({
  service_id: "",
  price: 0,
  currency: "INR",
  duration_minutes: 60,
  buffer_minutes: 0,
  service_modes: [],
});

const serviceModes = [
  {
    value: "ON_SITE",
    label: "On-site",
    description: "Customer visits your location.",
  },
  {
    value: "MOBILE",
    label: "Mobile",
    description: "Your team travels to the customer.",
  },
];

const selectedService = computed(() =>
  services.value.find(
    (service) => service.id === form.value.service_id,
  ),
);

async function load() {
  loading.value = true;
  error.value = null;

  try {
    const servicesResponse = await listServices(1, 100);

    services.value = servicesResponse.items.filter(
      (service) => service.is_active,
    );

    if (offeringId.value) {
      const offering = await getProviderServiceOffering(
        offeringId.value,
      );

      form.value = {
        service_id: offering.service_id,
        price: Number(offering.price),
        currency: offering.currency,
        duration_minutes: offering.duration_minutes,
        buffer_minutes: offering.buffer_minutes,
        service_modes: [...offering.service_modes],
      };
    }
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "Failed to load service offering.";
  } finally {
    loading.value = false;
  }
}

function toggleMode(mode: string) {
  const index = form.value.service_modes.indexOf(mode);

  if (index >= 0) {
    form.value.service_modes.splice(index, 1);
  } else {
    form.value.service_modes.push(mode);
  }
}

function goBack() {
  router.push({
    name: "provider-service-offerings",
  });
}

async function submit() {
  error.value = null;

  if (!form.value.service_id) {
    error.value = "Please select a service.";
    return;
  }

  if (form.value.price < 0) {
    error.value = "Price cannot be negative.";
    return;
  }

  if (form.value.duration_minutes <= 0) {
    error.value = "Duration must be greater than zero.";
    return;
  }

  if (form.value.service_modes.length === 0) {
    error.value = "Select at least one service mode.";
    return;
  }

  saving.value = true;

  try {
    if (offeringId.value) {
      await updateProviderServiceOffering(
        offeringId.value,
        form.value,
      );
    } else {
      await createProviderServiceOffering(form.value);
    }

    router.push({
      name: "provider-service-offerings",
    });
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "Failed to save service offering.";
  } finally {
    saving.value = false;
  }
}

onMounted(load);
</script>

<template>
  <section class="mx-auto max-w-3xl space-y-6">

    <!-- Header -->
    <div>
      <button
        type="button"
        class="mb-3 text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
        @click="goBack"
      >
        ← Back to service offerings
      </button>

      <h1 class="text-2xl font-semibold text-[var(--text-primary)]">
        {{ isEdit ? "Edit service offering" : "Add service offering" }}
      </h1>

      <p class="mt-1 text-sm text-[var(--text-secondary)]">
        Configure how your organization provides this service.
      </p>
    </div>

    <div
      v-if="loading"
      class="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-8 text-center"
    >
      Loading...
    </div>

    <form
      v-else
      class="space-y-6"
      @submit.prevent="submit"
    >
      <!-- Error -->
      <div
        v-if="error"
        class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
      >
        {{ error }}
      </div>

      <!-- Service -->
      <div class="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-6">
        <h2 class="text-base font-semibold">
          Service
        </h2>

        <p class="mt-1 text-sm text-[var(--text-secondary)]">
          Select a service from the ServiceHub catalog.
        </p>

        <div class="mt-5">
          <label class="block text-sm font-medium">
            Service
          </label>

          <select
            v-model="form.service_id"
            class="mt-2 w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] px-3 py-2.5 text-sm"
          >
            <option value="">
              Select a service
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

        <!-- Selected service info -->
        <div
          v-if="selectedService"
          class="mt-4 rounded-lg bg-[var(--background)] p-4"
        >
          <div class="text-sm font-medium">
            {{ selectedService.name }}
          </div>

          <div class="mt-1 text-xs text-[var(--text-secondary)]">
            {{ selectedService.slug }}
          </div>

          <p
            v-if="selectedService.description"
            class="mt-2 text-sm text-[var(--text-secondary)]"
          >
            {{ selectedService.description }}
          </p>
        </div>
      </div>

      <!-- Pricing -->
      <div class="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-6">
        <h2 class="text-base font-semibold">
          Pricing
        </h2>

        <div class="mt-5 grid gap-5 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium">
              Price
            </label>

            <input
              v-model.number="form.price"
              type="number"
              min="0"
              step="0.01"
              class="mt-2 w-full rounded-lg border border-[var(--border)] px-3 py-2.5 text-sm"
            />
          </div>

          <div>
            <label class="block text-sm font-medium">
              Currency
            </label>

            <select
              v-model="form.currency"
              class="mt-2 w-full rounded-lg border border-[var(--border)] px-3 py-2.5 text-sm"
            >
              <option value="INR">
                INR — Indian Rupee
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Timing -->
      <div class="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-6">
        <h2 class="text-base font-semibold">
          Timing
        </h2>

        <div class="mt-5 grid gap-5 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium">
              Service duration
            </label>

            <div class="relative mt-2">
              <input
                v-model.number="form.duration_minutes"
                type="number"
                min="1"
                max="1440"
                class="w-full rounded-lg border border-[var(--border)] px-3 py-2.5 pr-16 text-sm"
              />

              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[var(--text-secondary)]">
                minutes
              </span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium">
              Buffer time
            </label>

            <div class="relative mt-2">
              <input
                v-model.number="form.buffer_minutes"
                type="number"
                min="0"
                max="1440"
                class="w-full rounded-lg border border-[var(--border)] px-3 py-2.5 pr-16 text-sm"
              />

              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[var(--text-secondary)]">
                minutes
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Service modes -->
      <div class="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-6">
        <h2 class="text-base font-semibold">
          Service modes
        </h2>

        <p class="mt-1 text-sm text-[var(--text-secondary)]">
          Choose how customers can receive this service.
        </p>

        <div class="mt-5 grid gap-3">
          <label
            v-for="mode in serviceModes"
            :key="mode.value"
            class="flex cursor-pointer gap-3 rounded-lg border p-4 transition"
            :class="
              form.service_modes.includes(mode.value)
                ? 'border-[var(--primary)] bg-[var(--background)]'
                : 'border-[var(--border)]'
            "
          >
            <input
              type="checkbox"
              :checked="form.service_modes.includes(mode.value)"
              class="mt-1"
              @change="toggleMode(mode.value)"
            />

            <span>
              <span class="block text-sm font-medium">
                {{ mode.label }}
              </span>

              <span class="mt-1 block text-xs text-[var(--text-secondary)]">
                {{ mode.description }}
              </span>
            </span>
          </label>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-3">
        <button
          type="button"
          class="rounded-lg border border-[var(--border)] px-4 py-2.5 text-sm font-medium"
          @click="goBack"
        >
          Cancel
        </button>

        <button
          type="submit"
          :disabled="saving"
          class="rounded-lg bg-[var(--primary)] px-5 py-2.5 text-sm font-medium text-white disabled:opacity-50"
        >
          {{ saving ? "Saving..." : isEdit ? "Save changes" : "Create offering" }}
        </button>
      </div>
    </form>
  </section>
</template>