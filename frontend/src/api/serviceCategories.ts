import { apiRequest } from './client';

import type { ServiceCategory } from '../types/serviceCategory';

export function getServiceCategories(): Promise<ServiceCategory[]> {
  return apiRequest<ServiceCategory[]>('/service-categories', {
    method: 'GET',
  });
}
