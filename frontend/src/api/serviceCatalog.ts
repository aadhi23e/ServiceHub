import { apiRequest } from "./client";

export type RequirementType =
  | "TEXT"
  | "NUMBER"
  | "BOOLEAN"
  | "SELECT"
  | "DATE";

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

export interface ServiceRequirement {
  id: string;
  service_id: string;
  key: string;
  label: string;
  description: string | null;
  requirement_type: RequirementType;
  is_required: boolean;
  sort_order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CategoryCreateRequest {
  name: string;
  slug: string;
  description?: string | null;
}

export interface CategoryUpdateRequest {
  name?: string;
  slug?: string;
  description?: string | null;
}

export interface ServiceCreateRequest {
  category_id: string;
  name: string;
  slug: string;
  description?: string | null;
}

export interface ServiceUpdateRequest {
  category_id?: string;
  name?: string;
  slug?: string;
  description?: string | null;
}

export interface RequirementCreateRequest {
  key: string;
  label: string;
  description?: string | null;
  requirement_type: RequirementType;
  is_required: boolean;
  sort_order: number;
}

export interface RequirementUpdateRequest {
  key?: string;
  label?: string;
  description?: string | null;
  requirement_type?: RequirementType;
  is_required?: boolean;
  sort_order?: number;
}

/* -------------------------------------------------------------------------- */
/* Categories                                                                 */
/* -------------------------------------------------------------------------- */

export function listServiceCategories(): Promise<ServiceCategory[]> {
  return apiRequest<ServiceCategory[]>("/service-categories");
}

export function getServiceCategory(
  categoryId: string,
): Promise<ServiceCategory> {
  return apiRequest<ServiceCategory>(
    `/service-categories/${categoryId}`,
  );
}

export function createServiceCategory(
  payload: CategoryCreateRequest,
): Promise<ServiceCategory> {
  return apiRequest<ServiceCategory>("/service-categories", {
    method: "POST",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export function updateServiceCategory(
  categoryId: string,
  payload: CategoryUpdateRequest,
): Promise<ServiceCategory> {
  return apiRequest<ServiceCategory>(
    `/service-categories/${categoryId}`,
    {
      method: "PATCH",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    },
  );
}

export function activateServiceCategory(
  categoryId: string,
): Promise<ServiceCategory> {
  return apiRequest<ServiceCategory>(
    `/service-categories/${categoryId}/activate`,
    {
      method: "POST",
    },
  );
}

export function deactivateServiceCategory(
  categoryId: string,
): Promise<ServiceCategory> {
  return apiRequest<ServiceCategory>(
    `/service-categories/${categoryId}/deactivate`,
    {
      method: "POST",
    },
  );
}

/* -------------------------------------------------------------------------- */
/* Services                                                                   */
/* -------------------------------------------------------------------------- */

export function listServices(): Promise<Service[]> {
  return apiRequest<Service[]>("/services");
}

export function getService(serviceId: string): Promise<Service> {
  return apiRequest<Service>(`/services/${serviceId}`);
}

export function createService(
  payload: ServiceCreateRequest,
): Promise<Service> {
  return apiRequest<Service>("/services", {
    method: "POST",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export function updateService(
  serviceId: string,
  payload: ServiceUpdateRequest,
): Promise<Service> {
  return apiRequest<Service>(`/services/${serviceId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export function activateService(
  serviceId: string,
): Promise<Service> {
  return apiRequest<Service>(
    `/services/${serviceId}/activate`,
    {
      method: "POST",
    },
  );
}

export function deactivateService(
  serviceId: string,
): Promise<Service> {
  return apiRequest<Service>(
    `/services/${serviceId}/deactivate`,
    {
      method: "POST",
    },
  );
}

/* -------------------------------------------------------------------------- */
/* Requirements                                                               */
/* -------------------------------------------------------------------------- */

export function listServiceRequirements(
  serviceId: string,
): Promise<ServiceRequirement[]> {
  return apiRequest<ServiceRequirement[]>(
    `/services/${serviceId}/requirements`,
  );
}

export function createServiceRequirement(
  serviceId: string,
  payload: RequirementCreateRequest,
): Promise<ServiceRequirement> {
  return apiRequest<ServiceRequirement>(
    `/services/${serviceId}/requirements`,
    {
      method: "POST",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    },
  );
}

export function updateServiceRequirement(
  serviceId: string,
  requirementId: string,
  payload: RequirementUpdateRequest,
): Promise<ServiceRequirement> {
  return apiRequest<ServiceRequirement>(
    `/services/${serviceId}/requirements/${requirementId}`,
    {
      method: "PATCH",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    },
  );
}

export function activateServiceRequirement(
  serviceId: string,
  requirementId: string,
): Promise<ServiceRequirement> {
  return apiRequest<ServiceRequirement>(
    `/services/${serviceId}/requirements/${requirementId}/activate`,
    {
      method: "POST",
    },
  );
}

export function deactivateServiceRequirement(
  serviceId: string,
  requirementId: string,
): Promise<ServiceRequirement> {
  return apiRequest<ServiceRequirement>(
    `/services/${serviceId}/requirements/${requirementId}/deactivate`,
    {
      method: "POST",
    },
  );
}