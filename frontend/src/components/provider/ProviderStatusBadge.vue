<script setup lang="ts">
import { computed } from 'vue';

import type {
  MembershipStatus,
} from '../../types/provider';

const props = defineProps<{
  status: MembershipStatus;
}>();

const label = computed(() => {
  switch (props.status) {
    case 'ACTIVE':
      return 'Active';

    case 'INVITED':
      return 'Invited';

    case 'SUSPENDED':
      return 'Suspended';

    case 'REMOVED':
      return 'Removed';

    default:
      return props.status;
  }
});
</script>

<template>
  <span
    class="status-badge"
    :class="{
      'status-badge--success':
        status === 'ACTIVE',

      'status-badge--warning':
        status === 'INVITED',

      'status-badge--danger':
        status === 'SUSPENDED' ||
        status === 'REMOVED',
    }"
  >
    {{ label }}
  </span>
</template>