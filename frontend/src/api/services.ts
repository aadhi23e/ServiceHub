import { apiRequest } from "./client";

import type {
  Service,
  ServiceCreateRequest,
  ServiceListResponse,
  ServiceUpdateRequest,
} from "../types/service";

export function getMyServices(
  offset = 0,
  limit = 50,
): Promise<ServiceListResponse> {
  return apiRequest<ServiceListResponse>(
    `/providers/me/services?offset=${offset}&limit=${limit}`,
    {
      method: "GET",
    },
  );
}

export function getMyService(
  serviceId: number,
): Promise<Service> {
  return apiRequest<Service>(
    `/providers/me/services/${serviceId}`,
    {
      method: "GET",
    },
  );
}

export function createService(
  payload: ServiceCreateRequest,
): Promise<Service> {
  return apiRequest<Service>("/providers/me/services", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateService(
  serviceId: number,
  payload: ServiceUpdateRequest,
): Promise<Service> {
  return apiRequest<Service>(
    `/providers/me/services/${serviceId}`,
    {
      method: "PATCH",
      body: JSON.stringify(payload),
    },
  );
}

export function activateService(
  serviceId: number,
): Promise<Service> {
  return apiRequest<Service>(
    `/providers/me/services/${serviceId}/activate`,
    {
      method: "POST",
    },
  );
}

export function deactivateService(
  serviceId: number,
): Promise<Service> {
  return apiRequest<Service>(
    `/providers/me/services/${serviceId}/deactivate`,
    {
      method: "POST",
    },
  );
}