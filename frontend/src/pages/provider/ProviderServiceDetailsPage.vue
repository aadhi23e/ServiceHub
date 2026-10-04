<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue';

import {
  useRoute,
} from 'vue-router';

import {
  providerServiceOfferingsApi,
} from '../../api/providerServiceOfferings';

import {
  useProviderRole,
} from '../../composables/provider/useProviderRole';

import ServiceMemberList from '../../components/provider/ServiceMemberList.vue';

import ServiceMemberAssignModal from '../../components/provider/ServiceMemberAssignModal.vue';

import type {
  ProviderServiceOffering,
} from '../../types/provider';

const route = useRoute();

const {
  canManageServices,
} = useProviderRole();

const offering =
  ref<ProviderServiceOffering | null>(
    null,
  );

const loading = ref(true);
const error = ref<string | null>(null);
const showAssignModal = ref(false);

const offeringId = computed(
  () => String(route.params.offeringId),
);

async function loadOffering() {
  loading.value = true;
  error.value = null;

  try {
    offering.value =
      await providerServiceOfferingsApi.get(
        offeringId.value,
      );
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to load service.';
  } finally {
    loading.value = false;
  }
}

onMounted(loadOffering);
</script>

<template>
  <section class="space-y-6">
    <div
      v-if="loading"
      class="dashboard-card"
    >
      Loading service...
    </div>

    <div
      v-else-if="error"
      class="dashboard-card"
    >
      <p class="text-sm text-[var(--danger)]">
        {{ error }}
      </p>
    </div>

    <template v-else-if="offering">
      <header>
        <RouterLink
          to="/services"
          class="text-sm text-[var(--text-muted)]"
        >
          ← Services
        </RouterLink>

        <div
          class="mt-3 flex items-start justify-between gap-4"
        >
          <div>
            <h1
              class="text-2xl font-semibold"
            >
              {{ offering.service.name }}
            </h1>

            <p
              class="mt-1 text-sm text-[var(--text-muted)]"
            >
              {{ offering.service.slug }}
            </p>
          </div>

          <span
            class="status-badge"
            :class="{
              'status-badge--success':
                offering.is_active,
            }"
          >
            {{
              offering.is_active
                ? 'Active'
                : 'Inactive'
            }}
          </span>
        </div>
      </header>

      <section
        class="dashboard-card"
      >
        <h2 class="text-lg font-semibold">
          Service details
        </h2>

        <div
          class="mt-5 grid gap-5 sm:grid-cols-2 lg:grid-cols-4"
        >
          <div>
            <p
              class="text-xs text-[var(--text-muted)]"
            >
              Price
            </p>

            <p class="mt-1 font-medium">
              {{ offering.currency }}
              {{ offering.price }}
            </p>
          </div>

          <div>
            <p
              class="text-xs text-[var(--text-muted)]"
            >
              Duration
            </p>

            <p class="mt-1 font-medium">
              {{ offering.duration_minutes }}
              minutes
            </p>
          </div>

          <div>
            <p
              class="text-xs text-[var(--text-muted)]"
            >
              Buffer
            </p>

            <p class="mt-1 font-medium">
              {{ offering.buffer_minutes }}
              minutes
            </p>
          </div>

          <div>
            <p
              class="text-xs text-[var(--text-muted)]"
            >
              Modes
            </p>

            <p class="mt-1 font-medium">
              {{
                offering.service_modes.join(
                  ', ',
                )
              }}
            </p>
          </div>
        </div>
      </section>

      <ServiceMemberList
        :offering-id="offering.id"
        @assign="
          showAssignModal = true
        "
      />

      <ServiceMemberAssignModal
        v-if="showAssignModal"
        :offering-id="offering.id"
        @close="
          showAssignModal = false
        "
        @assigned="
          showAssignModal = false
        "
      />
    </template>
  </section>
</template>