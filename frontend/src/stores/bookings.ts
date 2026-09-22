import { computed, ref } from "vue";
import { defineStore } from "pinia";

import {
  cancelBooking,
  completeBooking,
  confirmBooking,
  createBooking,
  getAllBookings,
  getBooking,
  getMyBookings,
  getProviderBookings,
  rejectBooking,
  startBooking,
} from "../api/bookings";

import type {
  Booking,
  BookingCreateRequest,
} from "../types/booking";

export const useBookingStore = defineStore("bookings", () => {
  const bookings = ref<Booking[]>([]);
  const selectedBooking = ref<Booking | null>(null);

  const loading = ref(false);
  const actionLoading = ref(false);
  const error = ref<string | null>(null);

  const hasBookings = computed(
    () => bookings.value.length > 0,
  );

  function setError(value: unknown): void {
    if (value instanceof Error) {
      error.value = value.message;
      return;
    }

    error.value = "Something went wrong. Please try again.";
  }

  function clearError(): void {
    error.value = null;
  }

  function replaceBooking(updatedBooking: Booking): void {
    const index = bookings.value.findIndex(
      (booking) => booking.id === updatedBooking.id,
    );

    if (index !== -1) {
      bookings.value[index] = updatedBooking;
    }

    if (selectedBooking.value?.id === updatedBooking.id) {
      selectedBooking.value = updatedBooking;
    }
  }

  async function fetchMyBookings(): Promise<void> {
    loading.value = true;
    clearError();

    try {
      bookings.value = await getMyBookings();
    } catch (errorValue) {
      setError(errorValue);
    } finally {
      loading.value = false;
    }
  }

  async function fetchProviderBookings(): Promise<void> {
    loading.value = true;
    clearError();

    try {
      bookings.value = await getProviderBookings();
    } catch (errorValue) {
      setError(errorValue);
    } finally {
      loading.value = false;
    }
  }

  async function fetchAllBookings(): Promise<void> {
    loading.value = true;
    clearError();

    try {
      bookings.value = await getAllBookings();
    } catch (errorValue) {
      setError(errorValue);
    } finally {
      loading.value = false;
    }
  }

  async function fetchBooking(
    bookingId: number,
  ): Promise<Booking | null> {
    loading.value = true;
    clearError();

    try {
      const booking = await getBooking(bookingId);
      selectedBooking.value = booking;
      return booking;
    } catch (errorValue) {
      setError(errorValue);
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function create(
    payload: BookingCreateRequest,
  ): Promise<Booking | null> {
    actionLoading.value = true;
    clearError();

    try {
      const booking = await createBooking(payload);

      bookings.value.unshift(booking);

      return booking;
    } catch (errorValue) {
      setError(errorValue);
      return null;
    } finally {
      actionLoading.value = false;
    }
  }

  async function confirm(
    bookingId: number,
  ): Promise<boolean> {
    actionLoading.value = true;
    clearError();

    try {
      const booking = await confirmBooking(bookingId);
      replaceBooking(booking);
      return true;
    } catch (errorValue) {
      setError(errorValue);
      return false;
    } finally {
      actionLoading.value = false;
    }
  }

  async function reject(
    bookingId: number,
  ): Promise<boolean> {
    actionLoading.value = true;
    clearError();

    try {
      const booking = await rejectBooking(bookingId);
      replaceBooking(booking);
      return true;
    } catch (errorValue) {
      setError(errorValue);
      return false;
    } finally {
      actionLoading.value = false;
    }
  }

  async function start(
    bookingId: number,
  ): Promise<boolean> {
    actionLoading.value = true;
    clearError();

    try {
      const booking = await startBooking(bookingId);
      replaceBooking(booking);
      return true;
    } catch (errorValue) {
      setError(errorValue);
      return false;
    } finally {
      actionLoading.value = false;
    }
  }

  async function complete(
    bookingId: number,
  ): Promise<boolean> {
    actionLoading.value = true;
    clearError();

    try {
      const booking = await completeBooking(bookingId);
      replaceBooking(booking);
      return true;
    } catch (errorValue) {
      setError(errorValue);
      return false;
    } finally {
      actionLoading.value = false;
    }
  }

  async function cancel(
    bookingId: number,
  ): Promise<boolean> {
    actionLoading.value = true;
    clearError();

    try {
      const booking = await cancelBooking(bookingId);
      replaceBooking(booking);
      return true;
    } catch (errorValue) {
      setError(errorValue);
      return false;
    } finally {
      actionLoading.value = false;
    }
  }

  function clearSelectedBooking(): void {
    selectedBooking.value = null;
  }

  return {
    bookings,
    selectedBooking,

    loading,
    actionLoading,
    error,

    hasBookings,

    fetchMyBookings,
    fetchProviderBookings,
    fetchAllBookings,
    fetchBooking,

    create,
    confirm,
    reject,
    start,
    complete,
    cancel,

    clearError,
    clearSelectedBooking,
  };
});