<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

import { getServiceCategories } from '../../api/serviceCategories';
import { useServicesStore } from '../../stores/services';

import type { ServiceCategory } from '../../types/serviceCategory';

const router = useRouter();
const servicesStore = useServicesStore();

const categories = ref<ServiceCategory[]>([]);
const categoriesLoading = ref(false);
const categoriesError = ref<string | null>(null);

const form = reactive({
  category_id: 0,
  name: '',
  description: '',
  duration_minutes: 60,
  price: 0,
});

async function loadCategories() {
  categoriesLoading.value = true;
  categoriesError.value = null;

  try {
    categories.value = await getServiceCategories();
  } catch (err) {
    categoriesError.value =
      err instanceof Error ? err.message : 'Failed to load service categories.';
  } finally {
    categoriesLoading.value = false;
  }
}

async function submit() {
  await servicesStore.addService({
    category_id: form.category_id,
    name: form.name.trim(),
    description: form.description.trim() || null,
    duration_minutes: form.duration_minutes,
    price: form.price,
  });

  await router.push('/provider/services');
}

onMounted(loadCategories);
</script>

<template>
  <section class="provider-page">
    <div class="page-header">
      <div>
        <p class="page-eyebrow">Provider</p>

        <h1 class="page-title">Create service</h1>

        <p class="page-description">Add a service customers can book.</p>
      </div>
    </div>

    <form class="form-card" @submit.prevent="submit">
      <div class="form-grid">
        <div class="form-field form-field--full">
          <label for="name"> Service name </label>

          <input
            id="name"
            v-model="form.name"
            type="text"
            maxlength="200"
            required
            placeholder="e.g. Bathroom Pipe Repair"
          />
        </div>

        <div class="form-field">
          <label for="category"> Category </label>

          <select
            id="category"
            v-model.number="form.category_id"
            required
            :disabled="categoriesLoading"
          >
            <option disabled :value="0">
              {{ categoriesLoading ? 'Loading categories...' : 'Select a category' }}
            </option>

            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-field">
          <label for="duration"> Duration (minutes) </label>

          <input
            id="duration"
            v-model.number="form.duration_minutes"
            type="number"
            min="1"
            max="1440"
            required
          />
        </div>

        <div class="form-field">
          <label for="price"> Price </label>

          <div class="price-input">
            <span>₹</span>

            <input
              id="price"
              v-model.number="form.price"
              type="number"
              min="0"
              step="0.01"
              required
            />
          </div>
        </div>

        <div class="form-field form-field--full">
          <label for="description"> Description </label>

          <textarea
            id="description"
            v-model="form.description"
            rows="5"
            maxlength="5000"
            placeholder="Describe what this service includes."
          />
        </div>
      </div>

      <div v-if="categoriesError" class="form-error">
        {{ categoriesError }}
      </div>

      <div v-if="servicesStore.error" class="form-error">
        {{ servicesStore.error }}
      </div>

      <div class="form-actions">
        <button type="button" class="secondary-button" @click="router.back()">Cancel</button>

        <button
          type="submit"
          class="primary-button"
          :disabled="servicesStore.saving || categoriesLoading"
        >
          {{ servicesStore.saving ? 'Creating...' : 'Create service' }}
        </button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.provider-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-eyebrow {
  margin: 0 0 0.35rem;
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.page-title {
  margin: 0;
  color: var(--text-primary);
  font-size: clamp(1.5rem, 3vw, 2rem);
}

.page-description {
  margin: 0.45rem 0 0;
  color: var(--text-secondary);
}

.form-card {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--surface-primary);
  box-shadow: var(--shadow-sm);
  padding: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-field--full {
  grid-column: 1 / -1;
}

.form-field label {
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 600;
}

.form-field input,
.form-field select,
.form-field textarea {
  width: 100%;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--surface-secondary);
  color: var(--text-primary);
  padding: 0.75rem 0.875rem;
  outline: none;
}

.form-field textarea {
  resize: vertical;
}

.form-field input:focus,
.form-field select:focus,
.form-field textarea:focus {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px var(--accent-primary-soft);
}

.price-input {
  display: flex;
  align-items: center;
  overflow: hidden;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--surface-secondary);
}

.price-input span {
  padding-left: 0.875rem;
  color: var(--text-secondary);
}

.price-input input {
  border: 0;
  box-shadow: none !important;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.primary-button,
.secondary-button {
  border-radius: var(--radius-md);
  padding: 0.7rem 1rem;
  font-weight: 600;
  cursor: pointer;
}

.primary-button {
  border: 0;
  background: var(--accent-primary);
  color: var(--text-on-accent);
}

.secondary-button {
  border: 1px solid var(--border-default);
  background: var(--surface-secondary);
  color: var(--text-primary);
}

.form-error {
  margin-top: 1rem;
  color: var(--status-danger);
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

@media (max-width: 700px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-field--full {
    grid-column: auto;
  }

  .form-card {
    padding: 1rem;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>
