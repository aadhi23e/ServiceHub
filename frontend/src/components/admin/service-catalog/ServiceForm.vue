<script setup lang="ts">
import { reactive, ref } from "vue";
import {
  createService,
  updateService,
  type Service,
  type ServiceCategory,
} from "../../../api/serviceCatalog";

const props = defineProps<{
  service: Service | null;
  categories: ServiceCategory[];
}>();

const emit = defineEmits<{
  close: [];
  saved: [];
}>();

const editing = Boolean(props.service);

const form = reactive({
  category_id: props.service?.category_id ?? "",
  name: props.service?.name ?? "",
  slug: props.service?.slug ?? "",
  description: props.service?.description ?? "",
});

const loading = ref(false);
const errorMessage = ref("");

function generateSlug() {
  if (editing || !form.name.trim()) {
    return;
  }

  form.slug = form.name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

async function submit() {
  errorMessage.value = "";
  loading.value = true;

  try {
    if (props.service) {
      await updateService(props.service.id, {
        category_id: form.category_id,
        name: form.name.trim(),
        slug: form.slug.trim(),
        description: form.description.trim() || null,
      });
    } else {
      await createService({
        category_id: form.category_id,
        name: form.name.trim(),
        slug: form.slug.trim(),
        description: form.description.trim() || null,
      });
    }

    emit("saved");
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Unable to save service.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="modal-backdrop">
    <div
      class="modal-panel"
      role="dialog"
      aria-modal="true"
      aria-labelledby="service-form-title"
    >
      <div class="modal-header">
        <div>
          <p class="page-eyebrow">
            Service Catalog
          </p>

          <h2
            id="service-form-title"
            class="modal-title"
          >
            {{ editing ? "Edit service" : "Create service" }}
          </h2>
        </div>

        <button
          type="button"
          class="modal-close"
          @click="emit('close')"
        >
          ×
        </button>
      </div>

      <form
        class="space-y-5 p-6"
        @submit.prevent="submit"
      >
        <div
          v-if="errorMessage"
          class="alert-error"
        >
          {{ errorMessage }}
        </div>

        <div>
          <label
            for="service-category"
            class="form-label"
          >
            Category
          </label>

          <select
            id="service-category"
            v-model="form.category_id"
            class="form-input"
            required
          >
            <option
              value=""
              disabled
            >
              Select category
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

        <div>
          <label
            for="service-name"
            class="form-label"
          >
            Name
          </label>

          <input
            id="service-name"
            v-model="form.name"
            type="text"
            class="form-input"
            placeholder="Deep Home Cleaning"
            maxlength="100"
            required
            @blur="generateSlug"
          />
        </div>

        <div>
          <label
            for="service-slug"
            class="form-label"
          >
            Slug
          </label>

          <input
            id="service-slug"
            v-model="form.slug"
            type="text"
            class="form-input"
            placeholder="deep-home-cleaning"
            maxlength="120"
            required
          />
        </div>

        <div>
          <label
            for="service-description"
            class="form-label"
          >
            Description
          </label>

          <textarea
            id="service-description"
            v-model="form.description"
            class="form-input min-h-28 resize-y"
            placeholder="A detailed cleaning service..."
          />
        </div>

        <div class="modal-footer">
          <button
            type="button"
            class="btn-secondary"
            :disabled="loading"
            @click="emit('close')"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="btn-primary"
            :disabled="loading"
          >
            {{ loading ? "Saving..." : editing ? "Save changes" : "Create service" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<style scoped>
/* Service form modal */

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
  padding: var(--space-4);
  background: rgb(15 23 42 / 0.55);
}

.modal-panel {
  width: 100%;
  max-width: 560px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-lg);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-5) var(--space-6);
}

.modal-title {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.4;
}

.modal-close {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 1.5rem;
  line-height: 1;
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast),
    border-color var(--transition-fast);
}

.modal-close:hover {
  border-color: var(--color-border);
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.modal-close:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

/* Form */

.form-label {
  display: block;
  margin-bottom: 6px;
  color: var(--color-text-primary);
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.5;
}

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

.form-input:invalid:not(:placeholder-shown) {
  border-color: var(--color-danger);
}

/* Select */

select.form-input {
  cursor: pointer;
}

select.form-input:disabled {
  cursor: not-allowed;
}

/* Error */

.alert-error {
  border: 1px solid color-mix(in srgb, var(--color-danger) 30%, var(--color-border));
  border-radius: var(--radius-md);
  background: color-mix(in srgb, var(--color-danger) 8%, var(--color-surface));
  color: var(--color-danger);
  padding: 10px 12px;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Footer */

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-5);
}

/* Buttons */

.btn-primary {
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: var(--color-text-inverse);
  padding: 9px 14px;
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.5;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    opacity var(--transition-fast);
}

.btn-primary:hover:not(:disabled) {
  border-color: var(--color-primary-hover);
  background: var(--color-primary-hover);
}

.btn-primary:active:not(:disabled) {
  background: var(--color-primary-active);
}

.btn-primary:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.btn-primary:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-secondary {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  padding: 9px 14px;
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.5;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast);
}

.btn-secondary:hover:not(:disabled) {
  border-color: var(--color-border-strong);
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.btn-secondary:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.btn-secondary:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

/* Small screens */

@media (max-width: 640px) {
  .modal-backdrop {
    align-items: flex-start;
    padding: var(--space-3);
  }

  .modal-panel {
    margin-top: var(--space-4);
    border-radius: var(--radius-md);
  }

  .modal-header {
    padding: var(--space-4) var(--space-5);
  }

  .modal-title {
    font-size: 1.125rem;
  }

  .modal-footer {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .modal-footer .btn-primary,
  .modal-footer .btn-secondary {
    width: 100%;
  }
}
</style>