<script setup lang="ts">
import type { BookingStatus } from "../../types/booking";

defineProps<{
  status: BookingStatus;
}>();
</script>

<template>
  <span
    class="booking-status"
    :class="`booking-status--${status.toLowerCase()}`"
  >
    {{ status.replace("_", " ") }}
  </span>
</template>