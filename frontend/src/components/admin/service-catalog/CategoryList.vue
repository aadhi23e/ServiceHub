<script setup lang="ts">
import { computed, ref } from "vue";
import {
  activateServiceCategory,
  deactivateServiceCategory,
  type ServiceCategory,
  type Service,
} from "../../../api/serviceCatalog";

const props = defineProps<{
  categories: ServiceCategory[];
  services: Service[];
}>();

const emit = defineEmits<{
  edit: [category: ServiceCategory];
  changed: [];
  viewServices: [categoryId: string];
}>();

const search = ref("");
const processingId = ref<string | null>(null);

const filteredCategories = computed(() => {
  const query = search.value.trim().toLowerCase();

  if (!query) {
    return props.categories;
  }

  return props.categories.filter((category) => {
    return (
      category.name.toLowerCase().includes(query) ||
      category.slug.toLowerCase().includes(query) ||
      category.description?.toLowerCase().includes(query)
    );
  });
});

function serviceCount(categoryId: string) {
  return props.services.filter(
    (service) => service.category_id === categoryId,
  ).length;
}

async function toggleCategory(category: ServiceCategory) {
  processingId.value = category.id;

  try {
    if (category.is_active) {
      await deactivateServiceCategory(category.id);
    } else {
      await activateServiceCategory(category.id);
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
  <div class="space-y-5">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 class="section-title">
          Service categories
        </h2>

        <p class="section-description">
          Organize services into customer-facing categories.
        </p>
      </div>

      <div class="relative w-full sm:w-72">
        <input
          v-model="search"
          type="search"
          class="form-input"
          placeholder="Search categories..."
        />
      </div>
    </div>

    <div
      v-if="filteredCategories.length === 0"
      class="empty-state"
    >
      <div class="empty-state-icon">
        C
      </div>

      <h3 class="empty-state-title">
        No categories found
      </h3>

      <p class="empty-state-description">
        Create your first service category to start building the catalog.
      </p>
    </div>

    <div
      v-else
      class="overflow-x-auto"
    >
      <table class="data-table">
        <thead>
          <tr>
            <th>Category</th>
            <th>Slug</th>
            <th>Services</th>
            <th>Status</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="category in filteredCategories"
            :key="category.id"
          >
            <td>
              <div>
                <p class="font-semibold text-[var(--text-primary)]">
                  {{ category.name }}
                </p>

                <p
                  v-if="category.description"
                  class="mt-1 max-w-md truncate text-sm text-[var(--text-secondary)]"
                >
                  {{ category.description }}
                </p>
              </div>
            </td>

            <td>
              <code class="slug-text">
                {{ category.slug }}
              </code>
            </td>

            <td>
              <button
                type="button"
                class="table-link"
                @click="emit('viewServices', category.id)"
              >
                {{ serviceCount(category.id) }}
              </button>
            </td>

            <td>
              <span
                class="status-badge"
                :class="
                  category.is_active
                    ? 'status-active'
                    : 'status-inactive'
                "
              >
                {{ category.is_active ? "Active" : "Inactive" }}
              </span>
            </td>

            <td>
              <div class="flex justify-end gap-2">
                <button
                  type="button"
                  class="btn-table"
                  @click="emit('edit', category)"
                >
                  Edit
                </button>

                <button
                  type="button"
                  class="btn-table"
                  :disabled="processingId === category.id"
                  @click="toggleCategory(category)"
                >
                  {{
                    processingId === category.id
                      ? "..."
                      : category.is_active
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
  </div>
</template>
<style scoped>
/* Category list */

.section-title {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1.5;
}

.section-description {
  margin: 4px 0 0;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Search / form input */

.form-input {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-primary);
  padding: 10px 12px;
  font-size: 0.875rem;
  line-height: 1.5;
  outline: none;
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    background-color var(--transition-fast);
}

.form-input::placeholder {
  color: var(--color-text-muted);
}

.form-input:hover {
  border-color: var(--color-border-strong);
}

.form-input:focus {
  border-color: var(--color-focus-ring);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

/* Empty state */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 280px;
  padding: var(--space-8);
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  text-align: center;
}

.empty-state-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  margin-bottom: var(--space-4);
  border-radius: var(--radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 1rem;
  font-weight: 700;
}

.empty-state-title {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.5;
}

.empty-state-description {
  max-width: 420px;
  margin: var(--space-2) 0 0;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Data table */

.data-table {
  width: 100%;
  min-width: 760px;
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

.data-table tbody tr:last-child td {
  border-bottom: 0;
}

.data-table tbody tr {
  transition: background-color var(--transition-fast);
}

.data-table tbody tr:hover {
  background: var(--color-surface-hover);
}

/* Category text */

.slug-text {
  display: inline-block;
  max-width: 220px;
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

/* Service count link */

.table-link {
  border: 0;
  background: transparent;
  color: var(--color-primary);
  padding: 0;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.table-link:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}

.table-link:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
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