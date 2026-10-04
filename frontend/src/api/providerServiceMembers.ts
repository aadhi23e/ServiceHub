import { apiRequest } from './client';

import type {
  ProviderServiceMember,
  ProviderServiceMemberCreateRequest,
  ProviderServiceMemberListResponse,
} from '../types/provider';

const BASE_PATH = '/provider/service-offerings';

export const providerServiceMembersApi = {
  list(
    offeringId: string,
  ) {
    return apiRequest<ProviderServiceMemberListResponse>(
      `${BASE_PATH}/${offeringId}/members`,
    );
  },

  assign(
    offeringId: string,
    payload: ProviderServiceMemberCreateRequest,
  ) {
    return apiRequest<ProviderServiceMember>(
      `${BASE_PATH}/${offeringId}/members`,
      {
        method: 'POST',
        body: JSON.stringify(payload),
      },
    );
  },

  remove(
    offeringId: string,
    membershipId: string,
  ) {
    return apiRequest<void>(
      `${BASE_PATH}/${offeringId}/members/${membershipId}`,
      {
        method: 'DELETE',
      },
    );
  },
};