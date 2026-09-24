import type { UserRole } from './router';

export type UserStatus = 'ACTIVE' | 'SUSPENDED';

export interface AuthUser {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone: string | null;
  role: UserRole;
  status: UserStatus;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string | null;
  role: UserRole;
}

export interface RegisterResponse {
  user: AuthUser;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

export interface RefreshResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}
