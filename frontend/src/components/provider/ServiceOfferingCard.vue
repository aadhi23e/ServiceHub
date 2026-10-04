<script setup lang="ts">
import type {
  ProviderServiceOffering,
} from '../../types/provider';

defineProps<{
  offering: ProviderServiceOffering;
  canManage: boolean;
}>();

const emit = defineEmits<{
  activate: [offeringId: string];
  deactivate: [offeringId: string];
}>();
</script>

<template>
  <article class="dashboard-card">
    <div
      class="flex items-start justify-between gap-4"
    >
      <div>
        <h2 class="font-semibold">
          {{ offering.service.name }}
        </h2>

        <p class="mt-1 text-sm text-[var(--text-muted)]">
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

    <div
      class="mt-5 grid grid-cols-2 gap-4"
    >
      <div>
        <p class="text-xs text-[var(--text-muted)]">
          Price
        </p>

        <p class="mt-1 font-medium">
          {{ offering.currency }}
          {{ offering.price }}
        </p>
      </div>

      <div>
        <p class="text-xs text-[var(--text-muted)]">
          Duration
        </p>

        <p class="mt-1 font-medium">
          {{ offering.duration_minutes }}
          min
        </p>
      </div>
    </div>

    <div class="mt-5 flex flex-wrap gap-2">
      <span
        v-for="mode in offering.service_modes"
        :key="mode"
        class="mode-badge"
      >
        {{ mode }}
      </span>
    </div>

    <div
      class="mt-5 flex flex-wrap gap-3"
    >
      <RouterLink
        :to="`/services/${offering.id}`"
        class="button-secondary"
      >
        View
      </RouterLink>

      <button
        v-if="canManage"
        class="button-secondary"
        @click="
          offering.is_active
            ? emit(
                'deactivate',
                offering.id,
              )
            : emit(
                'activate',
                offering.id,
              )
        "
      >
        {{
          offering.is_active
            ? 'Deactivate'
            : 'Activate'
        }}
      </button>
    </div>
  </article>
</template>