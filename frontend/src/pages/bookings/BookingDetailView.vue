<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import BookingStatusBadge from '../../components/bookings/BookingStatusBadge.vue';
import { useBookingStore } from '../../stores/bookings';

const route = useRoute();
const router = useRouter();

const bookingStore = useBookingStore();

const bookingId = Number(route.params.bookingId);

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'full',
    timeStyle: 'short',
  }).format(new Date(value));
}

async function loadBooking(): Promise<void> {
  await bookingStore.fetchBooking(bookingId);
}

onMounted(loadBooking);
</script>

<template>
  <main class="booking-detail-page">
    <button type="button" @click="router.back()">← Back</button>

    <div v-if="bookingStore.loading" class="booking-detail-page__loading">Loading booking...</div>

    <div v-else-if="bookingStore.error" class="booking-detail-page__error" role="alert">
      {{ bookingStore.error }}
    </div>

    <section v-else-if="bookingStore.selectedBooking" class="booking-detail">
      <header class="booking-detail__header">
        <div>
          <p>Booking #{{ bookingStore.selectedBooking.id }}</p>

          <h1>Service #{{ bookingStore.selectedBooking.service_id }}</h1>
        </div>

        <BookingStatusBadge :status="bookingStore.selectedBooking.status" />
      </header>

      <dl class="booking-detail__information">
        <div>
          <dt>Provider</dt>
          <dd>#{{ bookingStore.selectedBooking.provider_id }}</dd>
        </div>

        <div>
          <dt>Customer</dt>
          <dd>#{{ bookingStore.selectedBooking.customer_id }}</dd>
        </div>

        <div>
          <dt>Start</dt>
          <dd>
            {{ formatDate(bookingStore.selectedBooking.start_at) }}
          </dd>
        </div>

        <div>
          <dt>End</dt>
          <dd>
            {{ formatDate(bookingStore.selectedBooking.end_at) }}
          </dd>
        </div>

        <div>
          <dt>Created</dt>
          <dd>
            {{ formatDate(bookingStore.selectedBooking.created_at) }}
          </dd>
        </div>
      </dl>

      <section v-if="bookingStore.selectedBooking.customer_notes" class="booking-detail__notes">
        <h2>Customer notes</h2>

        <p>
          {{ bookingStore.selectedBooking.customer_notes }}
        </p>
      </section>

      <section v-if="bookingStore.selectedBooking.provider_notes" class="booking-detail__notes">
        <h2>Provider notes</h2>

        <p>
          {{ bookingStore.selectedBooking.provider_notes }}
        </p>
      </section>
    </section>
  </main>
</template>
