export type BookingStatus =
  | "PENDING"
  | "CONFIRMED"
  | "REJECTED"
  | "CANCELLED"
  | "IN_PROGRESS"
  | "COMPLETED";

export interface Booking {
  id: number;

  customer_id: number;
  provider_id: number;
  service_id: number;

  start_at: string;
  end_at: string;

  status: BookingStatus;

  customer_notes: string | null;
  provider_notes: string | null;

  created_at: string;
  updated_at: string;

  cancelled_at: string | null;
  completed_at: string | null;
}

export interface BookingCreateRequest {
  provider_id: number;
  service_id: number;
  start_at: string;
  end_at: string;
  customer_notes?: string | null;
}