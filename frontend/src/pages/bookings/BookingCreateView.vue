<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import { useBookingStore } from "../../stores/bookings";

const router = useRouter();
const bookingStore = useBookingStore();

const providerId = ref("");
const serviceId = ref("");
const startAt = ref("");
const endAt = ref("");
const customerNotes = ref("");

const formError = ref<string | null>(null);

const isSubmitting = computed(
  () => bookingStore.actionLoading,
);

function validateForm(): boolean {
  formError.value = null;

  if (!providerId.value || !serviceId.value) {
    formError.value =
      "Provider and service are required.";
    return false;
  }

  if (!startAt.value || !endAt.value) {
    formError.value =
      "Start and end times are required.";
    return false;
  }

  const start = new Date(startAt.value);
  const end = new Date(endAt.value);

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    formError.value =
      "Please enter valid booking times.";
    return false;
  }

  if (start <= new Date()) {
    formError.value =
      "The booking start time must be in the future.";
    return false;
  }

  if (end <= start) {
    formError.value =
      "The end time must be later than the start time.";
    return false;
  }

  return true;
}

function toIsoDateTime(value: string): string {
  return new Date(value).toISOString();
}

async function submit(): Promise<void> {
  if (!validateForm()) {
    return;
  }

  const booking = await bookingStore.create({
    provider_id: Number(providerId.value),
    service_id: Number(serviceId.value),
    start_at: toIsoDateTime(startAt.value),
    end_at: toIsoDateTime(endAt.value),
    customer_notes:
      customerNotes.value.trim() || null,
  });

  if (!booking) {
    return;
  }

  router.replace({
    name: "booking-detail",
    params: {
      bookingId: booking.id,
    },
  });
}

function cancel(): void {
  router.back();
}
</script>

<template>
  <main class="booking-create-page">
    <header
      class="booking-create-page__header flex flex-col gap-5 sm:flex-row sm:items-start sm:gap-6"
    >
      <button
        type="button"
        class="booking-create-page__back-button"
        @click="cancel"
      >
        ← Back
      </button>

      <div>
        <p class="booking-create-page__eyebrow">
          ServiceHub
        </p>

        <h1>Book a service</h1>

        <p class="booking-create-page__description">
          Choose a provider, service, and time for your booking.
        </p>
      </div>
    </header>

    <form
      class="booking-form"
      @submit.prevent="submit"
    >
      <div
        v-if="formError"
        class="booking-form__error"
        role="alert"
      >
        {{ formError }}
      </div>

      <div
        v-if="bookingStore.error"
        class="booking-form__error"
        role="alert"
      >
        {{ bookingStore.error }}
      </div>

      <div class="booking-form__fields grid grid-cols-1 gap-5 md:grid-cols-2">
        <!-- Provider -->
        <div class="booking-form__field">
          <label for="provider-id">
            Provider ID
          </label>

          <input
            id="provider-id"
            v-model="providerId"
            type="number"
            min="1"
            required
            placeholder="Enter provider ID"
          />

          <p class="booking-form__help">
            Provider selection will be replaced with the provider
            catalog when that API is implemented.
          </p>
        </div>

        <!-- Service -->
        <div class="booking-form__field">
          <label for="service-id">
            Service ID
          </label>

          <input
            id="service-id"
            v-model="serviceId"
            type="number"
            min="1"
            required
            placeholder="Enter service ID"
          />

          <p class="booking-form__help">
            Service selection will be replaced with the service
            catalog when that API is implemented.
          </p>
        </div>

        <!-- Start -->
        <div class="booking-form__field">
          <label for="start-at">
            Start time
          </label>

          <input
            id="start-at"
            v-model="startAt"
            type="datetime-local"
            required
          />
        </div>

        <!-- End -->
        <div class="booking-form__field">
          <label for="end-at">
            End time
          </label>

          <input
            id="end-at"
            v-model="endAt"
            type="datetime-local"
            required
          />
        </div>

        <!-- Notes -->
        <div class="booking-form__field md:col-span-2">
          <label for="customer-notes">
            Notes
          </label>

          <textarea
            id="customer-notes"
            v-model="customerNotes"
            rows="5"
            maxlength="5000"
            placeholder="Add any information the provider should know..."
          ></textarea>
        </div>
      </div>

      <div
        class="booking-form__actions flex flex-col-reverse gap-3 sm:flex-row sm:justify-end"
      >
        <button
          type="button"
          class="booking-form__button booking-form__button--secondary"
          :disabled="isSubmitting"
          @click="cancel"
        >
          Cancel
        </button>

        <button
          type="submit"
          class="booking-form__button booking-form__button--primary"
          :disabled="isSubmitting"
        >
          <span v-if="isSubmitting">
            Creating booking...
          </span>

          <span v-else>
            Book service
          </span>
        </button>
      </div>
    </form>
  </main>
</template>

<style scoped>
/* =========================================================
   Page
   ========================================================= */

.booking-create-page {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 16px 12px;
}

/* =========================================================
   Header
   ========================================================= */

.booking-create-page__header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--color-border);
}

.booking-create-page__back-button {
  flex-shrink: 0;

  border: 0;
  padding: 8px 0;

  background: transparent;
  color: var(--color-text-secondary);

  font-size: 0.875rem;
  font-weight: 500;

  transition:
    color var(--transition-fast),
    transform var(--transition-fast);
}

.booking-create-page__back-button:hover {
  color: var(--color-text-primary);
}

.booking-create-page__back-button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 3px;
  border-radius: 4px;
}

.booking-create-page__eyebrow {
  margin: 0 0 6px;

  color: var(--color-primary);

  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.booking-create-page__header h1 {
  margin: 0;

  color: var(--color-text-primary);

  font-size: 1.875rem;
  font-weight: 700;
  line-height: 1.25;
}

.booking-create-page__description {
  margin: 8px 0 0;

  color: var(--color-text-secondary);

  font-size: 0.95rem;
  line-height: 1.6;
}

/* =========================================================
   Form
   ========================================================= */

.booking-form {
  padding: 24px;

  border: 1px solid var(--color-border);
  border-radius: 12px;

  background: var(--color-surface);

  box-shadow: var(--shadow-sm);
}

/* =========================================================
   Errors
   ========================================================= */

.booking-form__error {
  margin-bottom: 20px;
  padding: 12px 14px;

  border: 1px solid #fecaca;
  border-radius: 8px;

  background: #fef2f2;
  color: #b91c1c;

  font-size: 0.875rem;
  line-height: 1.5;
}

/* =========================================================
   Fields
   ========================================================= */

.booking-form__field {
  min-width: 0;
}

.booking-form__field label {
  display: block;
  margin-bottom: 7px;

  color: var(--color-text-primary);

  font-size: 0.875rem;
  font-weight: 600;
}

.booking-form__field input,
.booking-form__field textarea,
.booking-form__field select {
  display: block;
  width: 100%;

  border: 1px solid var(--color-border);
  border-radius: 8px;

  background: var(--color-surface);
  color: var(--color-text-primary);

  font-size: 0.9rem;
  line-height: 1.5;

  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    background-color var(--transition-fast);
}

.booking-form__field input,
.booking-form__field select {
  min-height: 44px;
  padding: 10px 12px;
}

.booking-form__field textarea {
  min-height: 120px;
  padding: 10px 12px;
  resize: vertical;
}

.booking-form__field input::placeholder,
.booking-form__field textarea::placeholder {
  color: var(--color-text-muted);
}

.booking-form__field input:hover,
.booking-form__field textarea:hover,
.booking-form__field select:hover {
  border-color: var(--color-border-strong);
}

.booking-form__field input:focus,
.booking-form__field textarea:focus,
.booking-form__field select:focus {
  border-color: var(--color-primary);

  outline: none;

  box-shadow:
    0 0 0 3px var(--color-primary-soft);
}

.booking-form__field input:disabled,
.booking-form__field textarea:disabled,
.booking-form__field select:disabled {
  cursor: not-allowed;

  background: var(--color-surface-secondary);
  color: var(--color-text-muted);

  opacity: 0.7;
}

/* =========================================================
   Help text
   ========================================================= */

.booking-form__help {
  margin: 6px 0 0;

  color: var(--color-text-muted);

  font-size: 0.75rem;
  line-height: 1.5;
}

/* =========================================================
   Actions
   ========================================================= */

.booking-form__actions {
  margin-top: 28px;
  padding-top: 20px;

  border-top: 1px solid var(--color-border);
}

.booking-form__button {
  min-height: 42px;

  border-radius: 8px;

  padding: 9px 16px;

  font-size: 0.875rem;
  font-weight: 600;

  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast),
    box-shadow var(--transition-fast);
}

.booking-form__button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.booking-form__button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Secondary */

.booking-form__button--secondary {
  border: 1px solid var(--color-border-strong);

  background: var(--color-surface);
  color: var(--color-text-secondary);
}

.booking-form__button--secondary:hover:not(:disabled) {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

/* Primary */

.booking-form__button--primary {
  border: 1px solid var(--color-primary);

  background: var(--color-primary);
  color: var(--color-text-inverse);

  box-shadow: var(--shadow-sm);
}

.booking-form__button--primary:hover:not(:disabled) {
  border-color: var(--color-primary-hover);
  background: var(--color-primary-hover);
}

.booking-form__button--primary:active:not(:disabled) {
  border-color: var(--color-primary-active);
  background: var(--color-primary-active);
}

/* =========================================================
   Responsive
   ========================================================= */

@media (max-width: 640px) {
  .booking-create-page {
    padding: 24px 16px;
  }

  .booking-create-page__header {
    margin-bottom: 24px;
    padding-bottom: 20px;
  }

  .booking-create-page__header h1 {
    font-size: 1.5rem;
  }

  .booking-form {
    padding: 20px 16px;
  }

  .booking-form__button {
    width: 100%;
  }
}
</style>