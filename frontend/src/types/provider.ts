export type ProviderStatus = 'ACTIVE' | 'SUSPENDED';

export interface Provider {
  id: number;
  user_id: number;
  business_name: string;
  description: string | null;
  phone: string | null;
  address: string | null;
  city: string | null;
  status: ProviderStatus;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface ProviderCreateRequest {
  business_name: string;
  description?: string | null;
  phone?: string | null;
  address?: string | null;
  city?: string | null;
  timezone?: string;
}

export interface ProviderUpdateRequest {
  business_name?: string;
  description?: string | null;
  phone?: string | null;
  address?: string | null;
  city?: string | null;
  timezone?: string;
}
