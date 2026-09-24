import * as authApi from '../api/auth';
import { useAuthStore } from '../stores/auth';
import { pinia } from '../app/pinia';

import type { LoginRequest, RegisterRequest } from '../types/auth';

const authStore = useAuthStore(pinia);

export async function signIn(payload: LoginRequest): Promise<void> {
  const response = await authApi.login(payload);

  authStore.setSession(response.user, response.access_token);
}

export async function signUp(payload: RegisterRequest): Promise<void> {
  await authApi.register(payload);
}

export async function loadCurrentUser(): Promise<void> {
  try {
    const user = await authApi.getCurrentUser();

    authStore.setUser(user);
  } catch {
    authStore.clearSession();

    throw new Error('Unable to load the current user.');
  }
}

export async function signOut(): Promise<void> {
  try {
    await authApi.logout();
  } finally {
    authStore.clearSession();
  }
}
