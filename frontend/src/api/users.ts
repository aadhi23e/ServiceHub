import { apiRequest } from "./client";
import type { User, UserUpdateRequest } from "../types/user";

export function getCurrentUser(): Promise<User> {
  return apiRequest<User>("/users/me", {
    method: "GET",
  });
}

export function updateCurrentUser(
  payload: UserUpdateRequest,
): Promise<User> {
  return apiRequest<User>("/users/me", {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}