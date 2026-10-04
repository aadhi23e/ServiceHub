<script setup lang="ts">
import {
  computed,
  ref,
} from 'vue';

import {
  providerMembershipsApi,
} from '../../api/providerMemberships';

import type {
  AgentType,
  ProviderMembershipRole,
} from '../../types/provider';

const emit = defineEmits<{
  close: [];
  invited: [];
}>();

const email = ref('');
const role =
  ref<ProviderMembershipRole>('AGENT');

const agentType =
  ref<AgentType | null>('MOBILE');

const submitting = ref(false);
const error = ref<string | null>(null);

const requiresAgentType = computed(
  () => role.value === 'AGENT',
);

async function submit() {
  error.value = null;

  const normalizedEmail =
    email.value.trim();

  if (!normalizedEmail) {
    error.value =
      'Email address is required.';
    return;
  }

  if (
    requiresAgentType.value &&
    !agentType.value
  ) {
    error.value =
      'Agent type is required.';
    return;
  }

  submitting.value = true;

  try {
    await providerMembershipsApi.invite({
      email: normalizedEmail,
      role: role.value,
      agent_type: requiresAgentType.value
        ? agentType.value
        : null,
    });

    emit('invited');
    emit('close');
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to send invitation.';
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <div class="modal-backdrop">
    <section class="modal-panel">
      <header>
        <h2 class="text-lg font-semibold">
          Invite team member
        </h2>

        <p
          class="mt-1 text-sm text-[var(--text-muted)]"
        >
          Invite a manager or agent to your
          organization.
        </p>
      </header>

      <form
        class="mt-6 space-y-5"
        @submit.prevent="submit"
      >
        <div>
          <label
            for="member-email"
            class="form-label"
          >
            Email
          </label>

          <input
            id="member-email"
            v-model="email"
            type="email"
            autocomplete="email"
            class="form-input mt-2"
            placeholder="name@example.com"
          />
        </div>

        <div>
          <label
            for="member-role"
            class="form-label"
          >
            Role
          </label>

          <select
            id="member-role"
            v-model="role"
            class="form-input mt-2"
          >
            <option value="AGENT">
              Agent
            </option>

            <option value="MANAGER">
              Manager
            </option>
          </select>
        </div>

        <div v-if="requiresAgentType">
          <label
            for="agent-type"
            class="form-label"
          >
            Agent type
          </label>

          <select
            id="agent-type"
            v-model="agentType"
            class="form-input mt-2"
          >
            <option value="MOBILE">
              Mobile
            </option>

            <option value="ON_SITE">
              On-site
            </option>

            <option value="HYBRID">
              Hybrid
            </option>
          </select>
        </div>

        <p
          v-if="error"
          class="text-sm text-[var(--danger)]"
        >
          {{ error }}
        </p>

        <footer
          class="flex justify-end gap-3"
        >
          <button
            type="button"
            class="button-secondary"
            @click="emit('close')"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="button-primary"
            :disabled="submitting"
          >
            {{
              submitting
                ? 'Sending...'
                : 'Send invitation'
            }}
          </button>
        </footer>
      </form>
    </section>
  </div>
</template>