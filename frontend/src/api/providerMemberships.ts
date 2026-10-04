import { apiRequest } from "./client";

import type {
  ProviderMember,
  ProviderMemberInvitationCreate,
  ProviderMemberListResponse,
  ProviderMembership,
  ProviderMembershipUpdate,
} from "../types/provider";

const BASE_PATH = "/provider/members";

export const providerMembershipsApi = {
  list() {
    return apiRequest<ProviderMemberListResponse>(
      BASE_PATH,
    );
  },

  get(membershipId: string) {
    return apiRequest<ProviderMember>(
      `${BASE_PATH}/${membershipId}`,
    );
  },

  invite(
    payload: ProviderMemberInvitationCreate,
  ) {
    return apiRequest<ProviderMembership>(
      `${BASE_PATH}/invite`,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );
  },

  update(
    membershipId: string,
    payload: ProviderMembershipUpdate,
  ) {
    return apiRequest<ProviderMembership>(
      `${BASE_PATH}/${membershipId}`,
      {
        method: "PATCH",
        body: JSON.stringify(payload),
      },
    );
  },

  remove(membershipId: string) {
    return apiRequest<ProviderMembership>(
      `${BASE_PATH}/${membershipId}`,
      {
        method: "DELETE",
      },
    );
  },
};