import { apiRequest } from './client';

import type {
  ProviderServiceOffering,
  ProviderServiceOfferingCreateRequest,
  ProviderServiceOfferingListResponse,
  ProviderServiceOfferingUpdateRequest,
} from '../types/provider';

const BASE_PATH = '/provider/service-offerings';

export const providerServiceOfferingsApi = {
  list(
    page = 1,
    pageSize = 20,
  ) {
    return apiRequest<ProviderServiceOfferingListResponse>(
      `${BASE_PATH}?page=${page}&page_size=${pageSize}`,
    );
  },

  get(
    offeringId: string,
  ) {
    return apiRequest<ProviderServiceOffering>(
      `${BASE_PATH}/${offeringId}`,
    );
  },

  create(
    payload: ProviderServiceOfferingCreateRequest,
  ) {
    return apiRequest<ProviderServiceOffering>(
      BASE_PATH,
      {
        method: 'POST',
        body: JSON.stringify(payload),
      },
    );
  },

  update(
    offeringId: string,
    payload: ProviderServiceOfferingUpdateRequest,
  ) {
    return apiRequest<ProviderServiceOffering>(
      `${BASE_PATH}/${offeringId}`,
      {
        method: 'PATCH',
        body: JSON.stringify(payload),
      },
    );
  },

  activate(
    offeringId: string,
  ) {
    return apiRequest<ProviderServiceOffering>(
      `${BASE_PATH}/${offeringId}/activate`,
      {
        method: 'POST',
      },
    );
  },

  deactivate(
    offeringId: string,
  ) {
    return apiRequest<ProviderServiceOffering>(
      `${BASE_PATH}/${offeringId}/deactivate`,
      {
        method: 'POST',
      },
    );
  },
};