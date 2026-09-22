import { apiRequest } from "./client";
import type {
  Booking,
  BookingCreateRequest,
} from "../types/booking";

export function createBooking(
  payload: BookingCreateRequest,
): Promise<Booking> {
  return apiRequest<Booking>("/bookings", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getMyBookings(): Promise<Booking[]> {
  return apiRequest<Booking[]>("/bookings/my", {
    method: "GET",
  });
}

export function getProviderBookings(): Promise<Booking[]> {
  return apiRequest<Booking[]>("/bookings/provider", {
    method: "GET",
  });
}

export function getAllBookings(): Promise<Booking[]> {
  return apiRequest<Booking[]>("/bookings", {
    method: "GET",
  });
}

export function getBooking(
  bookingId: number,
): Promise<Booking> {
  return apiRequest<Booking>(`/bookings/${bookingId}`, {
    method: "GET",
  });
}

export function confirmBooking(
  bookingId: number,
): Promise<Booking> {
  return apiRequest<Booking>(
    `/bookings/${bookingId}/confirm`,
    {
      method: "POST",
    },
  );
}

export function rejectBooking(
  bookingId: number,
): Promise<Booking> {
  return apiRequest<Booking>(
    `/bookings/${bookingId}/reject`,
    {
      method: "POST",
    },
  );
}

export function startBooking(
  bookingId: number,
): Promise<Booking> {
  return apiRequest<Booking>(
    `/bookings/${bookingId}/start`,
    {
      method: "POST",
    },
  );
}

export function completeBooking(
  bookingId: number,
): Promise<Booking> {
  return apiRequest<Booking>(
    `/bookings/${bookingId}/complete`,
    {
      method: "POST",
    },
  );
}

export function cancelBooking(
  bookingId: number,
): Promise<Booking> {
  return apiRequest<Booking>(
    `/bookings/${bookingId}/cancel`,
    {
      method: "POST",
    },
  );
}