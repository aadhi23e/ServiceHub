import { computed, ref } from 'vue';
import { defineStore } from 'pinia';

import type { ProviderMembership } from '../types/provider';

export const useProviderStore = defineStore(
  'provider',
  () => {
    /*
     * This is intentionally null for now.
     *
     * The current /auth/me response only gives us the
     * platform role:
     *
     *   CUSTOMER
     *   PROVIDER
     *   ADMIN
     *
     * It does not yet give us the organization role:
     *
     *   OWNER
     *   MANAGER
     *   AGENT
     *
     * Later the backend can provide the user's active
     * provider membership and this store can be populated.
     */
    const membership =
      ref<ProviderMembership | null>(null);

    const initialized = ref(false);

    const role = computed(
      () => membership.value?.role ?? null,
    );

    const organizationId = computed(
      () =>
        membership.value?.organization_id ?? null,
    );

    const isProviderMember = computed(
      () =>
        membership.value !== null &&
        membership.value.status === 'ACTIVE',
    );

    const isOwner = computed(
      () => role.value === 'OWNER',
    );

    const isManager = computed(
      () => role.value === 'MANAGER',
    );

    const isAgent = computed(
      () => role.value === 'AGENT',
    );

    const canManageServices = computed(
      () =>
        isOwner.value ||
        isManager.value,
    );

    const canManageTeam = computed(
      () =>
        isOwner.value ||
        isManager.value,
    );

    const canAssignServiceMembers = computed(
      () =>
        isOwner.value ||
        isManager.value,
    );

    function setMembership(
      value: ProviderMembership | null,
    ): void {
      membership.value = value;
    }

    function clearMembership(): void {
      membership.value = null;
    }

    function setInitialized(
      value: boolean,
    ): void {
      initialized.value = value;
    }

    function reset(): void {
      membership.value = null;
      initialized.value = false;
    }

    return {
      membership,
      initialized,

      role,
      organizationId,
      isProviderMember,

      isOwner,
      isManager,
      isAgent,

      canManageServices,
      canManageTeam,
      canAssignServiceMembers,

      setMembership,
      clearMembership,
      setInitialized,
      reset,
    };
  },
);