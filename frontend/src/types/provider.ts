export type ProviderMembershipRole =
  | 'OWNER'
  | 'MANAGER'
  | 'AGENT';

export type MembershipStatus =
  | 'INVITED'
  | 'ACTIVE'
  | 'SUSPENDED'
  | 'REMOVED';

export type AgentType =
  | 'MOBILE'
  | 'ON_SITE'
  | 'HYBRID';

export interface ProviderMembership {
  id: string;
  user_id: string;
  organization_id: string;
  role: ProviderMembershipRole;
  agent_type: AgentType | null;
  status: MembershipStatus;
  invited_at: string | null;
  joined_at: string | null;
  removed_at: string | null;
}

export interface ProviderMember {
  id: string;
  user_id: string;
  first_name: string;
  last_name: string;
  email: string;
  role: ProviderMembershipRole;
  agent_type: AgentType | null;
  status: MembershipStatus;
  invited_at: string | null;
  joined_at: string | null;
}

export interface ProviderMemberListResponse {
  items: ProviderMember[];
}

export interface ProviderMemberInvitationCreate {
  email: string;
  role: ProviderMembershipRole;
  agent_type?: AgentType | null;
}

export interface ProviderMembershipUpdate {
  role?: ProviderMembershipRole;
  agent_type?: AgentType | null;
}

export interface ProviderServiceOfferingService {
  id: string;
  name: string;
  slug: string;
  category_id: string;
}

export interface ProviderServiceOffering {
  id: string;
  organization_id: string;
  service_id: string;
  service: ProviderServiceOfferingService;
  price: string;
  currency: string;
  duration_minutes: number;
  buffer_minutes: number;
  service_modes: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProviderServiceOfferingListResponse {
  items: ProviderServiceOffering[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface ProviderServiceOfferingCreateRequest {
  service_id: string;
  price: string;
  currency: string;
  duration_minutes: number;
  buffer_minutes: number;
  service_modes: string[];
}

export interface ProviderServiceOfferingUpdateRequest {
  service_id?: string;
  price?: string;
  currency?: string;
  duration_minutes?: number;
  buffer_minutes?: number;
  service_modes?: string[];
}

/*
 * ProviderServiceMember is deliberately kept separate
 * from ProviderMembership.
 *
 * ProviderMembership:
 *   "John is an AGENT in this organization."
 *
 * ProviderServiceMember:
 *   "John is assigned to this particular service."
 */

export interface ProviderServiceMember {
  membership_id: string;
  user_id: string;
  first_name: string;
  last_name: string;
  email: string;
  role: ProviderMembershipRole;
  agent_type: AgentType | null;
  status: MembershipStatus;
}

export interface ProviderServiceMemberListResponse {
  items: ProviderServiceMember[];
}

export interface ProviderServiceMemberCreateRequest {
  provider_membership_id: string;
}