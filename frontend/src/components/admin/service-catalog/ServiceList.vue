<script setup lang="ts">
import { computed, ref } from "vue";
import {
  activateService,
  deactivateService,
  type Service,
  type ServiceCategory,
} from "../../../api/serviceCatalog";

const props = defineProps<{
  services: Service[];
  categories: ServiceCategory[];
}>();

const emit = defineEmits<{
  edit: [service: Service];
  changed: [];
}>();

const search = ref("");
const selectedCategory = ref("");
const processingId = ref<string | null>(null);

const filteredServices = computed(() => {
  const query = search.value.trim().toLowerCase();

  return props.services.filter((service) => {
    const matchesSearch =
      !query ||
      service.name.toLowerCase().includes(query) ||
      service.slug.toLowerCase().includes(query) ||
      service.description?.toLowerCase().includes(query);

    const matchesCategory =
      !selectedCategory.value ||
      service.category_id === selectedCategory.value;

    return matchesSearch && matchesCategory;
  });
});

function categoryName(categoryId: string) {
  return (
    props.categories.find(
      (category) => category.id === categoryId,
    )?.name ?? "Unknown category"
  );
}

async function toggleService(service: Service) {
  processingId.value = service.id;

  try {
    if (service.is_active) {
      await deactivateService(service.id);
    } else {
      await activateService(service.id);
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
    <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <h2 class="section-title">
          Services
        </h2>

        <p class="section-description">
          Define the services customers can discover.
        </p>
      </div>

      <div class="grid gap-3 sm:grid-cols-2">
        <input
          v-model="search"
          type="search"
          class="form-input"
          placeholder="Search services..."
        />

        <select
          v-model="selectedCategory"
          class="form-input"
        >
          <option value="">
            All categories
          </option>

          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>
    </div>

    <div
      v-if="filteredServices.length === 0"
      class="empty-state"
    >
      <div class="empty-state-icon">
        S
      </div>

      <h3 class="empty-state-title">
        No services found
      </h3>

      <p class="empty-state-description">
        Create a service or change your search filters.
      </p>
    </div>

    <div
      v-else
      class="overflow-x-auto"
    >
      <table class="data-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Category</th>
            <th>Slug</th>
            <th>Status</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="service in filteredServices"
            :key="service.id"
          >
            <td>
              <div>
                <p class="font-semibold text-[var(--text-primary)]">
                  {{ service.name }}
                </p>

                <p
                  v-if="service.description"
                  class="mt-1 max-w-md truncate text-sm text-[var(--text-secondary)]"
                >
                  {{ service.description }}
                </p>
              </div>
            </td>

            <td>
              {{ categoryName(service.category_id) }}
            </td>

            <td>
              <code class="slug-text">
                {{ service.slug }}
              </code>
            </td>

            <td>
              <span
                class="status-badge"
                :class="
                  service.is_active
                    ? 'status-active'
                    : 'status-inactive'
                "
              >
                {{ service.is_active ? "Active" : "Inactive" }}
              </span>
            </td>

            <td>
              <div class="flex justify-end gap-2">
                <button
                  type="button"
                  class="btn-table"
                  @click="emit('edit', service)"
                >
                  Edit
                </button>

                <button
                  type="button"
                  class="btn-table"
                  :disabled="processingId === service.id"
                  @click="toggleService(service)"
                >
                  {{
                    processingId === service.id
                      ? "..."
                      : service.is_active
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

<style lang="css" scoped>
/* Services list */

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

/* Search and category filter */

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

.form-input:disabled {
  cursor: not-allowed;
  background: var(--color-surface-secondary);
  color: var(--color-text-muted);
  opacity: 0.7;
}

select.form-input {
  cursor: pointer;
}

/* Empty state */

.empty-state {
  display: flex;
  min-height: 280px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  padding: var(--space-8);
  text-align: center;
}

.empty-state-icon {
  display: flex;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
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
  min-width: 780px;
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

/* Service slug */

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

/* Status */

.status-badge {
  display: inline-flex;
  min-height: 26px;
  align-items: center;
  border-radius: var(--radius-full);
  padding: 4px 9px;
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 1;
  white-space: nowrap;
}

.status-active {
  background: color-mix(
    in srgb,
    var(--color-success) 12%,
    transparent
  );
  color: var(--color-success);
}

.status-inactive {
  background: color-mix(
    in srgb,
    var(--color-text-muted) 14%,
    transparent
  );
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

/* Responsive filters */

@media (max-width: 640px) {
  .data-table {
    min-width: 720px;
  }

  .empty-state {
    min-height: 240px;
    padding: var(--space-6);
  }
}
</style>