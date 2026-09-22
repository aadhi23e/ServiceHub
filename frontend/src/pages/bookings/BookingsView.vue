<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";

import BookingCard from "../../components/bookings/BookingCard.vue";
import { useAuthStore } from "../../stores/auth.js";
import { useBookingStore } from "../../stores/bookings.js";
import type { Booking } from "../../types/booking.js";

const router = useRouter();

const authStore = useAuthStore();
const bookingStore = useBookingStore();

const isCustomer = computed(
  () => authStore.role === "CUSTOMER",
);

const isProvider = computed(
  () => authStore.role === "PROVIDER",
);

const isAdmin = computed(
  () => authStore.role === "ADMIN",
);

const pageTitle = computed(() => {
  if (isCustomer.value) return "My Bookings";
  if (isProvider.value) return "Provider Bookings";
  return "All Bookings";
});

async function loadBookings(): Promise<void> {
  if (isCustomer.value) {
    await bookingStore.fetchMyBookings();
    return;
  }

  if (isProvider.value) {
    await bookingStore.fetchProviderBookings();
    return;
  }

  if (isAdmin.value) {
    await bookingStore.fetchAllBookings();
  }
}

function viewBooking(booking: Booking): void {
  router.push({
    name: "booking-detail",
    params: {
      bookingId: booking.id,
    },
  });
}

async function cancelBooking(booking: Booking): Promise<void> {
  const confirmed = window.confirm(
    `Cancel booking #${booking.id}?`,
  );

  if (!confirmed) {
    return;
  }

  await bookingStore.cancel(booking.id);
}

async function confirmBooking(booking: Booking): Promise<void> {
  await bookingStore.confirm(booking.id);
}

async function rejectBooking(booking: Booking): Promise<void> {
  await bookingStore.reject(booking.id);
}

async function startBooking(booking: Booking): Promise<void> {
  await bookingStore.start(booking.id);
}

async function completeBooking(
  booking: Booking,
): Promise<void> {
  await bookingStore.complete(booking.id);
}

onMounted(loadBookings);
</script>

<template>
  <main class="bookings-page">
    <header
      class="bookings-page__header flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between"
    >
      <div class="bookings-page__heading">
        <p class="bookings-page__eyebrow">
          ServiceHub
        </p>

        <h1>{{ pageTitle }}</h1>

        <p class="bookings-page__description">
          Manage your service bookings and their current status.
        </p>
      </div>

      <button
        v-if="isCustomer"
        type="button"
        class="bookings-page__primary-button"
        @click="router.push({ name: 'booking-create' })"
      >
        Book a service
      </button>
    </header>

    <div
      v-if="bookingStore.error"
      class="bookings-page__error flex items-center justify-between gap-4"
      role="alert"
    >
      <span>{{ bookingStore.error }}</span>

      <button
        type="button"
        class="bookings-page__dismiss"
        @click="bookingStore.clearError"
      >
        Dismiss
      </button>
    </div>

    <div
      v-if="bookingStore.loading"
      class="bookings-page__loading"
      aria-live="polite"
    >
      Loading bookings...
    </div>

    <div
      v-else-if="!bookingStore.hasBookings"
      class="bookings-page__empty"
    >
      <h2>No bookings yet</h2>

      <p v-if="isCustomer">
        You don't have any bookings yet.
      </p>

      <p v-else>
        There are currently no bookings to display.
      </p>

      <button
        v-if="isCustomer"
        type="button"
        class="bookings-page__primary-button"
        @click="router.push({ name: 'booking-create' })"
      >
        Book a service
      </button>
    </div>

    <section
      v-else
      class="bookings-page__list grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3"
      aria-label="Bookings"
    >
      <BookingCard
        v-for="booking in bookingStore.bookings"
        :key="booking.id"
        :booking="booking"
        :can-cancel="
          isCustomer || isProvider || isAdmin
        "
        :can-manage="isProvider || isAdmin"
        :action-loading="bookingStore.actionLoading"
        @view="viewBooking"
        @cancel="cancelBooking"
        @confirm="confirmBooking"
        @reject="rejectBooking"
        @start="startBooking"
        @complete="completeBooking"
      />
    </section>
  </main>
</template>

<style scoped>
.bookings-page {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Header */

.bookings-page__header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--color-border);
}

.bookings-page__heading {
  min-width: 0;
}

.bookings-page__eyebrow {
  margin: 0 0 6px;
  color: var(--color-primary);
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.bookings-page__heading h1 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 1.875rem;
  font-weight: 700;
  line-height: 1.25;
}

.bookings-page__description {
  margin: 8px 0 0;
  color: var(--color-text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Primary button */

.bookings-page__primary-button {
  flex-shrink: 0;
  border: 1px solid var(--color-primary);
  border-radius: 8px;
  padding: 10px 16px;

  background: var(--color-primary);
  color: var(--color-text-inverse);

  font-size: 0.875rem;
  font-weight: 600;

  box-shadow: var(--shadow-sm);

  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    box-shadow var(--transition-fast);
}

.bookings-page__primary-button:hover {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}

.bookings-page__primary-button:active {
  background: var(--color-primary-active);
  border-color: var(--color-primary-active);
}

.bookings-page__primary-button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

/* Error */

.bookings-page__error {
  margin-bottom: 24px;
  padding: 14px 16px;

  border: 1px solid #fecaca;
  border-radius: 8px;

  background: #fef2f2;
  color: #b91c1c;

  font-size: 0.875rem;
  line-height: 1.5;
}

.bookings-page__dismiss {
  flex-shrink: 0;

  border: 0;
  padding: 0;

  background: transparent;
  color: inherit;

  font-size: inherit;
  font-weight: 600;

  text-decoration: underline;
  text-underline-offset: 2px;
}

.bookings-page__dismiss:hover {
  text-decoration: none;
}

/* Loading */

.bookings-page__loading {
  display: flex;
  min-height: 256px;
  align-items: center;
  justify-content: center;

  border: 1px solid var(--color-border);
  border-radius: 12px;

  background: var(--color-surface);
  color: var(--color-text-secondary);

  box-shadow: var(--shadow-sm);
}

/* Empty state */

.bookings-page__empty {
  display: flex;
  min-height: 320px;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  padding: 48px 24px;

  border: 1px dashed var(--color-border-strong);
  border-radius: 12px;

  background: var(--color-surface);

  text-align: center;
  box-shadow: var(--shadow-sm);
}

.bookings-page__empty h2 {
  margin: 0;

  color: var(--color-text-primary);

  font-size: 1.125rem;
  font-weight: 600;
}

.bookings-page__empty p {
  max-width: 420px;
  margin: 8px 0 20px;

  color: var(--color-text-secondary);

  font-size: 0.875rem;
  line-height: 1.6;
}

/* Booking list */

.bookings-page__list {
  width: 100%;
}

/* Responsive */

@media (max-width: 640px) {
  .bookings-page {
    padding: 24px 16px;
  }

  .bookings-page__header {
    margin-bottom: 24px;
    padding-bottom: 20px;
  }

  .bookings-page__heading h1 {
    font-size: 1.5rem;
  }

  .bookings-page__primary-button {
    width: 100%;
  }
}
</style>