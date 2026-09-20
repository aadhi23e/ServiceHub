import { computed, ref } from "vue";
import { defineStore } from "pinia";

import type { AuthUser } from "../types/auth";

export const useAuthStore = defineStore(
  "auth",
  () => {
    const user = ref<AuthUser | null>(null);

    const accessToken =
      ref<string | null>(null);

    const initialized = ref(false);

    const isAuthenticated = computed(
      () =>
        accessToken.value !== null &&
        user.value !== null,
    );

    const role = computed(
      () => user.value?.role ?? null,
    );

    const fullName = computed(() => {
      if (!user.value) {
        return "";
      }

      return `${user.value.first_name} ${user.value.last_name}`;
    });

    function setSession(
      newUser: AuthUser,
      newAccessToken: string,
    ): void {
      user.value = newUser;
      accessToken.value = newAccessToken;
    }

    function setUser(
      newUser: AuthUser,
    ): void {
      user.value = newUser;
    }

    function setAccessToken(
      newAccessToken: string,
    ): void {
      accessToken.value =
        newAccessToken;
    }

    function clearSession(): void {
      user.value = null;
      accessToken.value = null;
    }

    function setInitialized(): void {
      initialized.value = true;
    }

    return {
      user,
      accessToken,
      initialized,

      isAuthenticated,
      role,
      fullName,

      setSession,
      setUser,
      setAccessToken,
      clearSession,
      setInitialized,
    };
  },
);