<script setup lang="ts">
import {
  onMounted,
  ref,
} from 'vue';

import {
  providerMembershipsApi,
} from '../../api/providerMemberships';

import {
  useProviderRole,
} from '../../composables/provider/useProviderRole';

import TeamMemberCard from '../../components/provider/TeamMemberCard.vue';

import TeamMemberInviteModal from '../../components/provider/TeamMemberInviteModal.vue';

import type {
  ProviderMember,
} from '../../types/provider';

const {
  canManageTeam,
} = useProviderRole();

const members =
  ref<ProviderMember[]>([]);

const loading = ref(true);
const error = ref<string | null>(null);
const showInviteModal = ref(false);

async function loadMembers() {
  loading.value = true;
  error.value = null;

  try {
    const response =
      await providerMembershipsApi.list();

    members.value = response.items;
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to load team members.';
  } finally {
    loading.value = false;
  }
}

async function removeMember(
  membershipId: string,
) {
  try {
    await providerMembershipsApi.remove(
      membershipId,
    );

    members.value =
      members.value.filter(
        member =>
          member.id !== membershipId,
      );
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to remove member.';
  }
}

onMounted(loadMembers);
</script>

<template>
  <section class="space-y-6">
    <header
      class="flex items-start justify-between gap-4"
    >
      <div>
        <h1 class="text-2xl font-semibold">
          Team
        </h1>

        <p
          class="mt-1 text-sm text-[var(--text-muted)]"
        >
          Manage the members of your provider
          organization.
        </p>
      </div>

      <button
        v-if="canManageTeam"
        class="button-primary"
        @click="
          showInviteModal = true
        "
      >
        Invite member
      </button>
    </header>

    <div
      v-if="loading"
      class="dashboard-card"
    >
      Loading team...
    </div>

    <div
      v-else-if="error"
      class="dashboard-card"
    >
      <p class="text-sm text-[var(--danger)]">
        {{ error }}
      </p>

      <button
        class="button-secondary mt-4"
        @click="loadMembers"
      >
        Try again
      </button>
    </div>

    <div
      v-else-if="members.length === 0"
      class="dashboard-card"
    >
      <h2 class="font-semibold">
        No team members
      </h2>

      <p
        class="mt-1 text-sm text-[var(--text-muted)]"
      >
        Your organization does not have any
        additional members yet.
      </p>
    </div>

    <div
      v-else
      class="grid gap-5 lg:grid-cols-2"
    >
      <TeamMemberCard
        v-for="member in members"
        :key="member.id"
        :member="member"
        :can-manage="canManageTeam"
        @remove="removeMember"
      />
    </div>

    <TeamMemberInviteModal
      v-if="showInviteModal"
      @close="
        showInviteModal = false
      "
      @invited="loadMembers"
    />
  </section>
</template>