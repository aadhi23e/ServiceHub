<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue';

import {
  providerMembershipsApi,
} from '../../api/providerMemberships';

import {
  providerServiceMembersApi,
} from '../../api/providerServiceMembers';

import type {
  ProviderMember,
} from '../../types/provider';

const props = defineProps<{
  offeringId: string;
}>();

const emit = defineEmits<{
  close: [];
  assigned: [];
}>();

const members =
  ref<ProviderMember[]>([]);

const selectedMembershipId =
  ref('');

const loading = ref(true);
const submitting = ref(false);
const error = ref<string | null>(null);

const agents = computed(() =>
  members.value.filter(
    member =>
      member.role === 'AGENT' &&
      member.status === 'ACTIVE',
  ),
);

async function loadAgents() {
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
        : 'Unable to load agents.';
  } finally {
    loading.value = false;
  }
}

async function assignAgent() {
  if (!selectedMembershipId.value) {
    error.value =
      'Please select an agent.';
    return;
  }

  submitting.value = true;
  error.value = null;

  try {
    await providerServiceMembersApi.assign(
      props.offeringId,
      {
        provider_membership_id:
          selectedMembershipId.value,
      },
    );

    emit('assigned');
    emit('close');
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to assign agent.';
  } finally {
    submitting.value = false;
  }
}

onMounted(loadAgents);
</script>

<template>
  <div class="modal-backdrop">
    <section class="modal-panel">
      <header
        class="flex items-start justify-between gap-4"
      >
        <div>
          <h2 class="text-lg font-semibold">
            Assign agent
          </h2>

          <p
            class="mt-1 text-sm text-[var(--text-muted)]"
          >
            Select an active agent from your
            organization.
          </p>
        </div>

        <button
          class="button-ghost"
          @click="emit('close')"
        >
          Close
        </button>
      </header>

      <div class="mt-6">
        <div v-if="loading">
          Loading agents...
        </div>

        <template v-else>
          <label
            for="provider-agent"
            class="form-label"
          >
            Agent
          </label>

          <select
            id="provider-agent"
            v-model="selectedMembershipId"
            class="form-input mt-2"
          >
            <option
              value=""
              disabled
            >
              Select an agent
            </option>

            <option
              v-for="agent in agents"
              :key="agent.id"
              :value="agent.id"
            >
              {{ agent.first_name }}
              {{ agent.last_name }}
              —
              {{ agent.email }}
            </option>
          </select>

          <p
            v-if="agents.length === 0"
            class="mt-3 text-sm text-[var(--text-muted)]"
          >
            There are no active agents available
            to assign.
          </p>
        </template>

        <p
          v-if="error"
          class="mt-3 text-sm text-[var(--danger)]"
        >
          {{ error }}
        </p>
      </div>

      <footer
        class="mt-6 flex justify-end gap-3"
      >
        <button
          class="button-secondary"
          @click="emit('close')"
        >
          Cancel
        </button>

        <button
          class="button-primary"
          :disabled="
            submitting ||
            !selectedMembershipId
          "
          @click="assignAgent"
        >
          {{
            submitting
              ? 'Assigning...'
              : 'Assign agent'
          }}
        </button>
      </footer>
    </section>
  </div>
</template>