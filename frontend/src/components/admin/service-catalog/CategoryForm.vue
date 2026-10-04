<script setup lang="ts">
import { reactive, ref } from "vue";
import {
  createServiceCategory,
  updateServiceCategory,
  type ServiceCategory,
} from "../../../api/serviceCatalog";

const props = defineProps<{
  category: ServiceCategory | null;
}>();

const emit = defineEmits<{
  close: [];
  saved: [];
}>();

const editing = Boolean(props.category);

const form = reactive({
  name: props.category?.name ?? "",
  slug: props.category?.slug ?? "",
  description: props.category?.description ?? "",
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
    if (props.category) {
      await updateServiceCategory(props.category.id, {
        name: form.name.trim(),
        slug: form.slug.trim(),
        description: form.description.trim() || null,
      });
    } else {
      await createServiceCategory({
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
        : "Unable to save category.";
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
      aria-labelledby="category-form-title"
    >
      <div class="modal-header">
        <div>
          <p class="page-eyebrow">
            Service Catalog
          </p>

          <h2
            id="category-form-title"
            class="modal-title"
          >
            {{ editing ? "Edit category" : "Create category" }}
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
            for="category-name"
            class="form-label"
          >
            Name
          </label>

          <input
            id="category-name"
            v-model="form.name"
            type="text"
            class="form-input"
            placeholder="Home Cleaning"
            maxlength="100"
            required
            @blur="generateSlug"
          />
        </div>

        <div>
          <label
            for="category-slug"
            class="form-label"
          >
            Slug
          </label>

          <input
            id="category-slug"
            v-model="form.slug"
            type="text"
            class="form-input"
            placeholder="home-cleaning"
            maxlength="120"
            required
          />

          <p class="form-help">
            Used internally as the stable URL-friendly identifier.
          </p>
        </div>

        <div>
          <label
            for="category-description"
            class="form-label"
          >
            Description
          </label>

          <textarea
            id="category-description"
            v-model="form.description"
            class="form-input min-h-28 resize-y"
            placeholder="Services related to home cleaning..."
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
            {{ loading ? "Saving..." : editing ? "Save changes" : "Create category" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<style scoped>
/* =========================================================
   Modal Backdrop
   ========================================================= */

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: var(--space-4);

  background: rgb(15 23 42 / 0.55);

  overflow-y: auto;
}


/* =========================================================
   Modal Panel
   ========================================================= */

.modal-panel {
  width: 100%;
  max-width: 560px;

  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);

  background: var(--color-surface);
  color: var(--color-text-primary);

  box-shadow: var(--shadow-lg);

  overflow: hidden;
}


/* =========================================================
   Modal Header
   ========================================================= */

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);

  padding: var(--space-6);

  border-bottom: 1px solid var(--color-border);
}

.modal-title {
  margin-top: var(--space-1);

  color: var(--color-text-primary);

  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.35;
  letter-spacing: -0.015em;
}


/* =========================================================
   Close Button
   ========================================================= */

.modal-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  width: 36px;
  height: 36px;

  border: 1px solid transparent;
  border-radius: var(--radius-md);

  background: transparent;
  color: var(--color-text-muted);

  font-size: 1.5rem;
  font-weight: 400;
  line-height: 1;

  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast);
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


/* =========================================================
   Form
   ========================================================= */

.form-label {
  display: block;

  margin-bottom: var(--space-2);

  color: var(--color-text-primary);

  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.25;
}

.form-input {
  display: block;

  width: 100%;

  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);

  background: var(--color-surface);
  color: var(--color-text-primary);

  font-size: 0.875rem;
  line-height: 1.5;

  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    background-color var(--transition-fast);
}

input.form-input,
textarea.form-input {
  padding: 0.625rem 0.75rem;
}

.form-input::placeholder {
  color: var(--color-text-muted);
}

.form-input:hover {
  border-color: var(--color-border-strong);
}

.form-input:focus {
  border-color: var(--color-primary);

  outline: none;

  box-shadow: 0 0 0 3px
    color-mix(
      in srgb,
      var(--color-focus-ring) 25%,
      transparent
    );
}

.form-input:disabled {
  cursor: not-allowed;

  background: var(--color-surface-secondary);
  color: var(--color-text-muted);
}

.form-help {
  margin-top: var(--space-2);

  color: var(--color-text-muted);

  font-size: 0.75rem;
  line-height: 1.5;
}


/* =========================================================
   Error
   ========================================================= */

.alert-error {
  padding: var(--space-3) var(--space-4);

  border: 1px solid
    color-mix(
      in srgb,
      var(--color-danger) 25%,
      var(--color-border)
    );

  border-radius: var(--radius-md);

  background: color-mix(
    in srgb,
    var(--color-danger) 8%,
    var(--color-surface)
  );

  color: var(--color-danger);

  font-size: 0.875rem;
  line-height: 1.5;
}


/* =========================================================
   Modal Footer
   ========================================================= */

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);

  padding-top: var(--space-2);
}


/* =========================================================
   Buttons
   ========================================================= */

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-height: 40px;
  padding: 0 var(--space-4);

  border-radius: var(--radius-md);

  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1;

  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast),
    box-shadow var(--transition-fast),
    transform var(--transition-fast);
}

.btn-primary {
  border: 1px solid var(--color-primary);
  background: var(--color-primary);
  color: var(--color-text-inverse);
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover:not(:disabled) {
  border-color: var(--color-primary-hover);
  background: var(--color-primary-hover);
}

.btn-primary:active:not(:disabled) {
  border-color: var(--color-primary-active);
  background: var(--color-primary-active);
  transform: translateY(1px);
}

.btn-secondary {
  border: 1px solid var(--color-border-strong);
  background: var(--color-surface);
  color: var(--color-text-primary);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-surface-hover);
}

.btn-primary:focus-visible,
.btn-secondary:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.btn-primary:disabled,
.btn-secondary:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}


/* =========================================================
   Responsive
   ========================================================= */

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
    padding: var(--space-4);
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