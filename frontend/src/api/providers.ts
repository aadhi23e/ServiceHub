import { apiRequest } from './client';

import type { Provider, ProviderCreateRequest, ProviderUpdateRequest } from '../types/provider';

export function createProvider(payload: ProviderCreateRequest): Promise<Provider> {
  return apiRequest<Provider>('/providers/create', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getMyProvider(): Promise<Provider> {
  return apiRequest<Provider>('/providers/me', {
    method: 'GET',
  });
}

export function updateMyProvider(payload: ProviderUpdateRequest): Promise<Provider> {
  return apiRequest<Provider>('/providers/me', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}
