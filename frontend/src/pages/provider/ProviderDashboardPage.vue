<script setup lang="ts">
import { computed } from 'vue';

import { useAuthStore } from '../../stores/auth';
import { useProviderStore } from '../../stores/provider';

import ProviderRoleBadge from '../../components/provider/ProviderRoleBadge.vue';

const auth = useAuthStore();
const provider = useProviderStore();

const displayName = computed(() => {
  if (!auth.user) {
    return '';
  }

  return `${auth.user.first_name} ${auth.user.last_name}`.trim();
});
</script>

<template>
  <section class="space-y-6">
    <header>
      <div
        class="flex flex-wrap items-center gap-3"
      >
        <h1 class="text-2xl font-semibold">
          Provider Dashboard
        </h1>

        <ProviderRoleBadge
          :role="provider.role"
        />
      </div>

      <p
        class="mt-2 text-sm text-[var(--text-muted)]"
      >
        Welcome back, {{ displayName }}.
      </p>
    </header>

    <div
      v-if="!provider.membership"
      class="dashboard-card"
    >
      <h2 class="font-semibold">
        Provider organization
      </h2>

      <p
        class="mt-2 text-sm text-[var(--text-muted)]"
      >
        Your organization membership has not
        been loaded yet.
      </p>

      <p
        class="mt-1 text-sm text-[var(--text-muted)]"
      >
        Organization-specific controls will
        appear once the provider membership
        API is connected.
      </p>
    </div>

    <div
      v-else
      class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4"
    >
      <RouterLink
        to="/services"
        class="dashboard-card dashboard-card--interactive"
      >
        <p class="text-sm text-[var(--text-muted)]">
          Services
        </p>

        <p class="mt-2 font-semibold">
          Manage services
        </p>
      </RouterLink>

      <RouterLink
        v-if="provider.canManageTeam"
        to="/team"
        class="dashboard-card dashboard-card--interactive"
      >
        <p class="text-sm text-[var(--text-muted)]">
          Team
        </p>

        <p class="mt-2 font-semibold">
          Manage team
        </p>
      </RouterLink>

      <RouterLink
        to="/availability"
        class="dashboard-card dashboard-card--interactive"
      >
        <p class="text-sm text-[var(--text-muted)]">
          Availability
        </p>

        <p class="mt-2 font-semibold">
          Manage availability
        </p>
      </RouterLink>

      <RouterLink
        to="/bookings"
        class="dashboard-card dashboard-card--interactive"
      >
        <p class="text-sm text-[var(--text-muted)]">
          Bookings
        </p>

        <p class="mt-2 font-semibold">
          View bookings
        </p>
      </RouterLink>
    </div>
  </section>
</template>