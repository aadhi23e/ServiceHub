import {
  apiRequest,
} from "./client";

import type {
  AuthUser,
  LoginRequest,
  LoginResponse,
  RefreshResponse,
  RegisterRequest,
  RegisterResponse,
} from "../types/auth";

export function login(
  payload: LoginRequest,
): Promise<LoginResponse> {
  return apiRequest<LoginResponse>(
    "/auth/login",
    {
      method: "POST",
      body: JSON.stringify(payload),
      skipAuth: true,
    },
  );
}

export function register(
  payload: RegisterRequest,
): Promise<RegisterResponse> {
  return apiRequest<RegisterResponse>(
    "/auth/register",
    {
      method: "POST",
      body: JSON.stringify(payload),
      skipAuth: true,
    },
  );
}

export function refresh(): Promise<RefreshResponse> {
  return apiRequest<RefreshResponse>(
    "/auth/refresh",
    {
      method: "POST",
      skipAuth: true,
    },
  );
}

export function getCurrentUser(): Promise<AuthUser> {
  return apiRequest<AuthUser>(
    "/auth/me",
    {
      method: "GET",
    },
  );
}

export function logout(): Promise<void> {
  return apiRequest<void>(
    "/auth/logout",
    {
      method: "POST",
      skipAuth: true,
    },
  );
}