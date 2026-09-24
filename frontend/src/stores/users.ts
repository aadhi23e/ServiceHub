import { defineStore } from 'pinia';
import { getCurrentUser, updateCurrentUser } from '../api/users';
import type { User, UserUpdateRequest } from '../types/user';

interface UserState {
  user: User | null;
  loading: boolean;
  saving: boolean;
  error: string | null;
  initialized: boolean;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    loading: false,
    saving: false,
    error: null,
    initialized: false,
  }),

  actions: {
    async fetchCurrentUser(): Promise<User> {
      this.loading = true;
      this.error = null;

      try {
        const user = await getCurrentUser();

        this.user = user;
        this.initialized = true;

        return user;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to load your profile.';

        throw error;
      } finally {
        this.loading = false;
      }
    },

    async updateProfile(payload: UserUpdateRequest): Promise<User> {
      this.saving = true;
      this.error = null;

      try {
        const user = await updateCurrentUser(payload);

        this.user = user;

        return user;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Unable to update your profile.';

        throw error;
      } finally {
        this.saving = false;
      }
    },

    clear(): void {
      this.user = null;
      this.error = null;
      this.initialized = false;
    },
  },
});
