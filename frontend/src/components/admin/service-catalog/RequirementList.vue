<script setup lang="ts">
import { ref } from "vue";
import {
  activateServiceRequirement,
  deactivateServiceRequirement,
  type ServiceRequirement,
} from "../../../api/serviceCatalog";

defineProps<{
  serviceId: string;
  requirements: ServiceRequirement[];
}>();

const emit = defineEmits<{
  edit: [requirement: ServiceRequirement];
  changed: [];
}>();

const processingId = ref<string | null>(null);

async function toggleRequirement(
  serviceId: string,
  requirement: ServiceRequirement,
) {
  processingId.value = requirement.id;

  try {
    if (requirement.is_active) {
      await deactivateServiceRequirement(
        serviceId,
        requirement.id,
      );
    } else {
      await activateServiceRequirement(
        serviceId,
        requirement.id,
      );
    }

    emit("changed");
  } catch (error) {
    console.error(error);
  } finally {
    processingId.value = null;
  }
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="data-table">
      <thead>
        <tr>
          <th>Requirement</th>
          <th>Type</th>
          <th>Required</th>
          <th>Order</th>
          <th>Status</th>
          <th class="text-right">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="requirement in requirements"
          :key="requirement.id"
        >
          <td>
            <div>
              <p class="font-semibold text-[var(--text-primary)]">
                {{ requirement.label }}
              </p>

              <code class="slug-text">
                {{ requirement.key }}
              </code>
            </div>
          </td>

          <td>
            <span class="type-badge">
              {{ requirement.requirement_type }}
            </span>
          </td>

          <td>
            {{ requirement.is_required ? "Required" : "Optional" }}
          </td>

          <td>
            {{ requirement.sort_order }}
          </td>

          <td>
            <span
              class="status-badge"
              :class="
                requirement.is_active
                  ? 'status-active'
                  : 'status-inactive'
              "
            >
              {{ requirement.is_active ? "Active" : "Inactive" }}
            </span>
          </td>

          <td>
            <div class="flex justify-end gap-2">
              <button
                type="button"
                class="btn-table"
                @click="emit('edit', requirement)"
              >
                Edit
              </button>

              <button
                type="button"
                class="btn-table"
                :disabled="processingId === requirement.id"
                @click="
                  toggleRequirement(
                    serviceId,
                    requirement,
                  )
                "
              >
                {{
                  processingId === requirement.id
                    ? "..."
                    : requirement.is_active
                      ? "Deactivate"
                      : "Activate"
                }}
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<style scoped>
/* Service requirements table */

.data-table {
  width: 100%;
  min-width: 820px;
  border-collapse: separate;
  border-spacing: 0;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  color: var(--color-text-primary);
}

.data-table th {
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 1.5;
  text-align: left;
  letter-spacing: 0.025em;
  text-transform: uppercase;
  white-space: nowrap;
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  vertical-align: middle;
}

.data-table tbody tr {
  transition: background-color var(--transition-fast);
}

.data-table tbody tr:hover {
  background: var(--color-surface-hover);
}

.data-table tbody tr:last-child td {
  border-bottom: 0;
}

/* Requirement type */

.type-badge {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  padding: 4px 9px;
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
}

/* Requirement key */

.slug-text {
  display: inline-block;
  max-width: 220px;
  margin-top: 4px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  padding: 3px 7px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.75rem;
  line-height: 1.4;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Status */

.status-badge {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  border-radius: var(--radius-full);
  padding: 4px 9px;
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 1;
  white-space: nowrap;
}

.status-active {
  background: color-mix(in srgb, var(--color-success) 12%, transparent);
  color: var(--color-success);
}

.status-inactive {
  background: color-mix(in srgb, var(--color-text-muted) 14%, transparent);
  color: var(--color-text-muted);
}

/* Table actions */

.btn-table {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  padding: 6px 10px;
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1.4;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast);
}

.btn-table:hover:not(:disabled) {
  border-color: var(--color-border-strong);
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.btn-table:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.btn-table:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}
</style>