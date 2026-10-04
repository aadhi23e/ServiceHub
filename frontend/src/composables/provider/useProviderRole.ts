import { computed } from 'vue';

import { useProviderStore } from '../../stores/provider';

export function useProviderRole() {
  const provider = useProviderStore();

  const role = computed(
    () => provider.role,
  );

  const isOwner = computed(
    () => provider.isOwner,
  );

  const isManager = computed(
    () => provider.isManager,
  );

  const isAgent = computed(
    () => provider.isAgent,
  );

  const canManageServices = computed(
    () => provider.canManageServices,
  );

  const canManageTeam = computed(
    () => provider.canManageTeam,
  );

  const canAssignServiceMembers = computed(
    () => provider.canAssignServiceMembers,
  );

  return {
    role,
    isOwner,
    isManager,
    isAgent,

    canManageServices,
    canManageTeam,
    canAssignServiceMembers,
  };
}