<script setup lang="ts">
import { computed } from 'vue';

import type { Booking } from '../../types/booking';
import BookingStatusBadge from './BookingStatusBadge.vue';

const props = defineProps<{
  booking: Booking;
  canCancel?: boolean;
  canManage?: boolean;
  actionLoading?: boolean;
}>();

const emit = defineEmits<{
  view: [booking: Booking];
  cancel: [booking: Booking];
  confirm: [booking: Booking];
  reject: [booking: Booking];
  start: [booking: Booking];
  complete: [booking: Booking];
}>();

const canCancelBooking = computed(() => {
  return props.canCancel && ['PENDING', 'CONFIRMED'].includes(props.booking.status);
});

const canConfirmBooking = computed(() => {
  return props.canManage && props.booking.status === 'PENDING';
});

const canRejectBooking = computed(() => {
  return props.canManage && props.booking.status === 'PENDING';
});

const canStartBooking = computed(() => {
  return props.canManage && props.booking.status === 'CONFIRMED';
});

const canCompleteBooking = computed(() => {
  return props.canManage && props.booking.status === 'IN_PROGRESS';
});

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value));
}
</script>

<template>
  <article class="booking-card">
    <div class="booking-card__header">
      <div>
        <p class="booking-card__id">Booking #{{ booking.id }}</p>

        <h3>Service #{{ booking.service_id }}</h3>
      </div>

      <BookingStatusBadge :status="booking.status" />
    </div>

    <div class="booking-card__details">
      <div>
        <span>Start</span>
        <strong>{{ formatDate(booking.start_at) }}</strong>
      </div>

      <div>
        <span>End</span>
        <strong>{{ formatDate(booking.end_at) }}</strong>
      </div>

      <div>
        <span>Provider</span>
        <strong>#{{ booking.provider_id }}</strong>
      </div>
    </div>

    <p v-if="booking.customer_notes" class="booking-card__notes">
      {{ booking.customer_notes }}
    </p>

    <div class="booking-card__actions">
      <button type="button" @click="emit('view', booking)">View</button>

      <button
        v-if="canCancelBooking"
        type="button"
        :disabled="actionLoading"
        @click="emit('cancel', booking)"
      >
        Cancel
      </button>

      <button
        v-if="canConfirmBooking"
        type="button"
        :disabled="actionLoading"
        @click="emit('confirm', booking)"
      >
        Confirm
      </button>

      <button
        v-if="canRejectBooking"
        type="button"
        :disabled="actionLoading"
        @click="emit('reject', booking)"
      >
        Reject
      </button>

      <button
        v-if="canStartBooking"
        type="button"
        :disabled="actionLoading"
        @click="emit('start', booking)"
      >
        Start
      </button>

      <button
        v-if="canCompleteBooking"
        type="button"
        :disabled="actionLoading"
        @click="emit('complete', booking)"
      >
        Complete
      </button>
    </div>
  </article>
</template>
