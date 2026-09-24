<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { useServicesStore } from '../../stores/services';
import { getServiceCategories } from '../../api/serviceCategories';

import type { ServiceCategory } from '../../types/serviceCategory';

const route = useRoute();
const router = useRouter();
const servicesStore = useServicesStore();

const categories = ref<ServiceCategory[]>([]);
const categoriesLoading = ref(false);
const categoriesError = ref<string | null>(null);

const loadingService = ref(true);
const pageError = ref<string | null>(null);
const successMessage = ref('');

const form = reactive({
  category_id: 0,
  name: '',
  description: '',
  duration_minutes: 60,
  price: 0,
});

const serviceId = Number(route.params.serviceId);

function populateForm() {
  const service = servicesStore.selectedService;

  if (!service) {
    return;
  }

  form.category_id = service.category_id;
  form.name = service.name;
  form.description = service.description ?? '';
  form.duration_minutes = service.duration_minutes;
  form.price = Number(service.price);
}

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

async function loadService() {
  loadingService.value = true;
  pageError.value = null;

  try {
    await servicesStore.fetchService(serviceId);

    if (!servicesStore.selectedService) {
      pageError.value = 'Service could not be found.';
      return;
    }

    populateForm();
  } catch (err) {
    pageError.value = err instanceof Error ? err.message : 'Failed to load service.';
  } finally {
    loadingService.value = false;
  }
}

async function saveService() {
  successMessage.value = '';

  try {
    await servicesStore.editService(serviceId, {
      category_id: form.category_id,
      name: form.name.trim(),
      description: form.description.trim() || null,
      duration_minutes: form.duration_minutes,
      price: form.price,
    });

    successMessage.value = 'Service updated successfully.';
  } catch {
    // The store exposes the API error.
  }
}

function goBack() {
  router.push('/provider/services');
}

onMounted(async () => {
  await Promise.all([loadCategories(), loadService()]);
});
</script>

<template>
  <section class="provider-page">
    <!-- Header -->
    <div class="page-header">
      <div>
        <p class="page-eyebrow">Provider</p>

        <h1 class="page-title">Edit service</h1>

        <p class="page-description">Update the details of your service.</p>
      </div>

      <button type="button" class="secondary-button" @click="goBack">Back to services</button>
    </div>

    <!-- Loading -->
    <div v-if="loadingService" class="state-card">
      <div class="loading-spinner"></div>

      <p>Loading service...</p>
    </div>

    <!-- Page error -->
    <div v-else-if="pageError" class="state-card state-card--error">
      <h2>Unable to load service</h2>

      <p>
        {{ pageError }}
      </p>

      <button type="button" class="secondary-button" @click="goBack">Back to services</button>
    </div>

    <!-- Form -->
    <form v-else class="form-card" @submit.prevent="saveService">
      <div class="form-grid">
        <!-- Name -->
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

        <!-- Category -->
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

          <p v-if="categoriesError" class="field-error">
            {{ categoriesError }}
          </p>
        </div>

        <!-- Duration -->
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

        <!-- Price -->
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

        <!-- Description -->
        <div class="form-field form-field--full">
          <label for="description"> Description </label>

          <textarea
            id="description"
            v-model="form.description"
            rows="6"
            maxlength="5000"
            placeholder="Describe what this service includes."
          />

          <span class="character-count"> {{ form.description.length }}/5000 </span>
        </div>
      </div>

      <!-- API Error -->
      <div v-if="servicesStore.error" class="form-error">
        {{ servicesStore.error }}
      </div>

      <!-- Success -->
      <div v-if="successMessage" class="form-success">
        {{ successMessage }}
      </div>

      <!-- Actions -->
      <div class="form-actions">
        <button
          type="button"
          class="secondary-button"
          :disabled="servicesStore.saving"
          @click="goBack"
        >
          Cancel
        </button>

        <button
          type="submit"
          class="primary-button"
          :disabled="servicesStore.saving || categoriesLoading"
        >
          {{ servicesStore.saving ? 'Saving...' : 'Save changes' }}
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

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
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
  font-weight: 700;
}

.page-description {
  margin: 0.45rem 0 0;
  color: var(--text-secondary);
}

.form-card,
.state-card {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--surface-primary);
  box-shadow: var(--shadow-sm);
}

.form-card {
  padding: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}

.form-field {
  position: relative;
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
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.form-field textarea {
  min-height: 130px;
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

.price-input:focus-within {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px var(--accent-primary-soft);
}

.price-input span {
  padding-left: 0.875rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.price-input input {
  border: 0;
  box-shadow: none !important;
}

.character-count {
  align-self: flex-end;
  margin-top: -0.25rem;
  color: var(--text-tertiary);
  font-size: 0.75rem;
}

.field-error {
  margin: 0;
  color: var(--status-danger);
  font-size: 0.8rem;
}

.form-error {
  margin-top: 1.25rem;
  color: var(--status-danger);
}

.form-success {
  margin-top: 1.25rem;
  color: var(--status-success);
  font-weight: 500;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.primary-button,
.secondary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  border-radius: var(--radius-md);
  padding: 0.7rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    opacity 0.2s ease,
    background-color 0.2s ease,
    border-color 0.2s ease;
}

.primary-button {
  border: 1px solid var(--accent-primary);
  background: var(--accent-primary);
  color: var(--text-on-accent);
}

.secondary-button {
  border: 1px solid var(--border-default);
  background: var(--surface-secondary);
  color: var(--text-primary);
}

.primary-button:hover:not(:disabled) {
  opacity: 0.9;
}

.secondary-button:hover:not(:disabled) {
  border-color: var(--accent-primary);
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.state-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 220px;
  padding: 2rem;
  text-align: center;
}

.state-card h2 {
  margin: 0 0 0.5rem;
  color: var(--text-primary);
}

.state-card p {
  margin: 0 0 1rem;
  color: var(--text-secondary);
}

.state-card--error {
  color: var(--status-danger);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  margin-bottom: 0.75rem;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 700px) {
  .page-header {
    align-items: stretch;
    flex-direction: column;
  }

  .form-card {
    padding: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-field--full {
    grid-column: auto;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>
