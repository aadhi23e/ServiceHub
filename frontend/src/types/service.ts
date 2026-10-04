// export interface Service {
//   id: number;
//   provider_id: number;
//   category_id: number;
//   name: string;
//   description: string | null;
//   duration_minutes: number;
//   price: string | number;
//   is_active: boolean;
//   created_at: string;
//   updated_at: string;
// }
export interface ServiceCategory {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Service {
  id: string;
  category_id: string;
  name: string;
  slug: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ServiceListResponse {
  items: Service[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}
export interface ServiceCreateRequest {
  category_id: number;
  name: string;
  description?: string | null;
  duration_minutes: number;
  price: number;
}

export interface ServiceUpdateRequest {
  category_id?: number;
  name?: string;
  description?: string | null;
  duration_minutes?: number;
  price?: number;
}

// export interface ServiceListResponse {
//   items: Service[];
//   total: number;
//   offset: number;
//   limit: number;
// }
