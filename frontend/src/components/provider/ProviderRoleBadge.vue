<script setup lang="ts">
import { computed } from 'vue';

import type {
  ProviderMembershipRole,
} from '../../types/provider';

const props = defineProps<{
  role: ProviderMembershipRole | null;
}>();

const label = computed(() => {
  switch (props.role) {
    case 'OWNER':
      return 'Owner';

    case 'MANAGER':
      return 'Manager';

    case 'AGENT':
      return 'Agent';

    default:
      return 'Provider';
  }
});
</script>

<template>
  <span class="status-badge">
    {{ label }}
  </span>
</template>