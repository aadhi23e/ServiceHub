<script setup lang="ts">
import { onMounted, ref } from "vue";

import {
  addProviderServiceMember,
  listProviderServiceMembers,
  removeProviderServiceMember,
  type ProviderServiceMember,
} from "../../../api/providerServiceOfferings";

interface AvailableMember {
  id: string;
  user_id: string;
  role: string;
  status: string;
  agent_type: string | null;
  full_name?: string;
}

const props = defineProps<{
  offeringId: string;
  members: AvailableMember[];
}>();

const emit = defineEmits<{
  changed: [];
}>();

const assignments = ref<
  ProviderServiceMember[]
>([]);

const selectedMembershipId = ref("");
const loading = ref(true);
const processing = ref(false);
const errorMessage = ref("");

async function loadMembers() {
  loading.value = true;

  try {
    assignments.value =
      await listProviderServiceMembers(
        props.offeringId,
      );
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Unable to load service members.";
  } finally {
    loading.value = false;
  }
}

const assignedMembershipIds = () =>
  new Set(
    assignments.value.map(
      (assignment) =>
        assignment.provider_membership_id,
    ),
  );

async function assignMember() {
  if (!selectedMembershipId.value) {
    return;
  }

  processing.value = true;
  errorMessage.value = "";

  try {
    await addProviderServiceMember(
      props.offeringId,
      selectedMembershipId.value,
    );

    selectedMembershipId.value = "";

    await loadMembers();

    emit("changed");
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Unable to assign member.";
  } finally {
    processing.value = false;
  }
}

async function removeMember(
  membershipId: string,
) {
  processing.value = true;
  errorMessage.value = "";

  try {
    await removeProviderServiceMember(
      props.offeringId,
      membershipId,
    );

    await loadMembers();

    emit("changed");
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Unable to remove member.";
  } finally {
    processing.value = false;
  }
}

onMounted(loadMembers);
</script>

<template>
  <div class="space-y-5">
    <div>
      <h3
        class="font-semibold text-[var(--text-primary)]"
      >
        Assigned team members
      </h3>

      <p
        class="mt-1 text-sm text-[var(--text-secondary)]"
      >
        Assign active agents who can perform this service.
      </p>
    </div>

    <div
      v-if="errorMessage"
      class="alert-error"
    >
      {{ errorMessage }}
    </div>

    <div
      v-if="!loading && members.length"
      class="flex flex-col gap-3 sm:flex-row"
    >
      <select
        v-model="selectedMembershipId"
        class="form-input flex-1"
      >
        <option value="">
          Select an agent
        </option>

        <option
          v-for="member in members.filter(
            (member) =>
              !assignedMembershipIds().has(
                member.id,
              ),
          )"
          :key="member.id"
          :value="member.id"
        >
          {{
            member.full_name ??
            member.user_id
          }}
        </option>
      </select>

      <button
        type="button"
        class="btn-primary"
        :disabled="
          !selectedMembershipId ||
          processing
        "
        @click="assignMember"
      >
        Assign
      </button>
    </div>

    <div
      v-if="loading"
      class="text-sm text-[var(--text-secondary)]"
    >
      Loading team members...
    </div>

    <div
      v-else-if="assignments.length === 0"
      class="rounded-lg border border-dashed border-[var(--border-subtle)] p-6 text-center"
    >
      <p
        class="text-sm text-[var(--text-secondary)]"
      >
        No team members are assigned to this service.
      </p>
    </div>

    <div
      v-else
      class="space-y-2"
    >
      <div
        v-for="assignment in assignments"
        :key="assignment.id"
        class="flex items-center justify-between rounded-lg border border-[var(--border-subtle)] px-4 py-3"
      >
        <div>
          <p
            class="text-sm font-medium text-[var(--text-primary)]"
          >
            {{
              members.find(
                (member) =>
                  member.id ===
                  assignment.provider_membership_id,
              )?.full_name ??
              assignment.provider_membership_id
            }}
          </p>

          <p
            class="text-xs text-[var(--text-secondary)]"
          >
            Assigned
          </p>
        </div>

        <button
          type="button"
          class="btn-secondary"
          :disabled="processing"
          @click="
            removeMember(
              assignment.provider_membership_id,
            )
          "
        >
          Remove
        </button>
      </div>
    </div>
  </div>
</template>