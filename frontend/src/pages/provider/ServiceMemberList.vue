<script setup lang="ts">
import { onMounted, ref } from "vue";

import { providerServiceMembersApi } from "../../api/providerServiceMembers";
import { useProviderRole } from "../../composables/provider/useProviderRole";
import type {
  ProviderServiceMember,
} from "../../types/provider";

const props = defineProps<{
  offeringId: string;
}>();

const emit = defineEmits<{
  assign: [];
}>();

const {
  canAssignServiceMembers,
} = useProviderRole();

const members = ref<ProviderServiceMember[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

async function loadMembers() {
  loading.value = true;
  error.value = null;

  try {
    const response =
      await providerServiceMembersApi.list(
        props.offeringId,
      );

    members.value = response.items;
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "Unable to load assigned agents.";
  } finally {
    loading.value = false;
  }
}

async function removeMember(
  member: ProviderServiceMember,
) {
  try {
    await providerServiceMembersApi.remove(
      props.offeringId,
      member.id,
    );

    members.value = members.value.filter(
      item => item.id !== member.id,
    );
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "Unable to remove agent.";
  }
}

onMounted(loadMembers);

defineExpose({
  loadMembers,
});
</script>

<template>
  <section class="dashboard-card">
    <div class="flex items-center justify-between gap-4">
      <div>
        <h2 class="text-lg font-semibold">
          Assigned agents
        </h2>

        <p class="mt-1 text-sm text-[var(--text-muted)]">
          Agents assigned to this service offering.
        </p>
      </div>

      <button
        v-if="canAssignServiceMembers"
        class="button-primary"
        @click="emit('assign')"
      >
        Assign agent
      </button>
    </div>

    <div
      v-if="loading"
      class="mt-6 text-sm text-[var(--text-muted)]"
    >
      Loading agents...
    </div>

    <p
      v-else-if="error"
      class="mt-6 text-sm text-[var(--danger)]"
    >
      {{ error }}
    </p>

    <div
      v-else-if="members.length === 0"
      class="mt-6 rounded-lg border border-[var(--border)] p-5"
    >
      <p class="text-sm text-[var(--text-muted)]">
        No agents are assigned to this service.
      </p>
    </div>

    <div
      v-else
      class="mt-6 divide-y divide-[var(--border)]"
    >
      <div
        v-for="member in members"
        :key="member.id"
        class="flex items-center justify-between gap-4 py-4"
      >
        <div>
          <p class="font-medium">
            {{ member.first_name }}
            {{ member.last_name }}
          </p>

          <p class="text-sm text-[var(--text-muted)]">
            {{ member.email }}
          </p>
        </div>

        <button
          v-if="canAssignServiceMembers"
          class="button-danger"
          @click="removeMember(member)"
        >
          Remove
        </button>
      </div>
    </div>
  </section>
</template>