<script setup lang="ts">
import ProviderRoleBadge from './ProviderRoleBadge.vue';
import ProviderStatusBadge from './ProviderStatusBadge.vue';

import type {
  ProviderMember,
} from '../../types/provider';

defineProps<{
  member: ProviderMember;
  canManage: boolean;
}>();

const emit = defineEmits<{
  edit: [member: ProviderMember];
  remove: [membershipId: string];
}>();
</script>

<template>
  <article class="dashboard-card">
    <div
      class="flex items-start justify-between gap-4"
    >
      <div>
        <h2 class="font-semibold">
          {{ member.first_name }}
          {{ member.last_name }}
        </h2>

        <p
          class="mt-1 text-sm text-[var(--text-muted)]"
        >
          {{ member.email }}
        </p>
      </div>

      <ProviderStatusBadge
        :status="member.status"
      />
    </div>

    <div
      class="mt-4 flex flex-wrap items-center gap-2"
    >
      <ProviderRoleBadge
        :role="member.role"
      />

      <span
        v-if="member.agent_type"
        class="mode-badge"
      >
        {{ member.agent_type }}
      </span>
    </div>

    <div
      v-if="canManage"
      class="mt-5 flex gap-3"
    >
      <button
        class="button-secondary"
        @click="emit('edit', member)"
      >
        Edit
      </button>

      <button
        class="button-danger"
        @click="
          emit(
            'remove',
            member.id,
          )
        "
      >
        Remove
      </button>
    </div>
  </article>
</template>