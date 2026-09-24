<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useProviderStore } from '../../stores/provider';

const providerStore = useProviderStore();

const successMessage = ref('');

const form = reactive({
  business_name: '',
  description: '',
  phone: '',
  address: '',
  city: '',
  timezone: '',
});

function populateForm() {
  if (!providerStore.provider) {
    return;
  }

  form.business_name = providerStore.provider.business_name;

  form.description = providerStore.provider.description ?? '';

  form.phone = providerStore.provider.phone ?? '';

  form.address = providerStore.provider.address ?? '';

  form.city = providerStore.provider.city ?? '';

  form.timezone = providerStore.provider.timezone;
}

async function saveProfile() {
  successMessage.value = '';

  await providerStore.updateProvider({
    business_name: form.business_name.trim(),
    description: form.description.trim() || null,
    phone: form.phone.trim() || null,
    address: form.address.trim() || null,
    city: form.city.trim() || null,
    timezone: form.timezone.trim(),
  });

  successMessage.value = 'Provider profile updated successfully.';
}

onMounted(async () => {
  if (!providerStore.provider) {
    await providerStore.fetchProvider();
  }

  populateForm();
});
</script>

<template>
  <section class="provider-page">
    <div class="page-header">
      <div>
        <p class="page-eyebrow">Provider</p>
        <h1 class="page-title">Business profile</h1>
        <p class="page-description">Manage the business information customers see on ServiceHub.</p>
      </div>
    </div>

    <div v-if="providerStore.loading" class="state-card">Loading provider profile...</div>

    <div v-else-if="providerStore.error" class="state-card state-card--error">
      {{ providerStore.error }}
    </div>

    <form v-else class="provider-form-card" @submit.prevent="saveProfile">
      <div class="form-grid">
        <div class="form-field form-field--full">
          <label for="business-name"> Business name </label>

          <input
            id="business-name"
            v-model="form.business_name"
            type="text"
            maxlength="200"
            required
          />
        </div>

        <div class="form-field form-field--full">
          <label for="description"> Description </label>

          <textarea id="description" v-model="form.description" rows="5" maxlength="5000" />
        </div>

        <div class="form-field">
          <label for="phone">Phone</label>

          <input id="phone" v-model="form.phone" type="tel" maxlength="30" />
        </div>

        <div class="form-field">
          <label for="city">City</label>

          <input id="city" v-model="form.city" type="text" maxlength="100" />
        </div>

        <div class="form-field form-field--full">
          <label for="address">Address</label>

          <textarea id="address" v-model="form.address" rows="3" maxlength="500" />
        </div>

        <div class="form-field">
          <label for="timezone">Timezone</label>

          <input id="timezone" v-model="form.timezone" type="text" maxlength="100" />
        </div>
      </div>

      <div v-if="successMessage" class="form-success">
        {{ successMessage }}
      </div>

      <div v-if="providerStore.error" class="form-error">
        {{ providerStore.error }}
      </div>

      <div class="form-actions">
        <button class="primary-button" type="submit" :disabled="providerStore.updating">
          {{ providerStore.updating ? 'Saving...' : 'Save changes' }}
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

.provider-form-card,
.state-card {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--surface-primary);
  box-shadow: var(--shadow-sm);
}

.provider-form-card {
  padding: 1.5rem;
}

.form-grid {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
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
  resize: vertical;
}

.form-field input:focus,
.form-field textarea:focus {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px var(--accent-primary-soft);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.primary-button {
  border: 0;
  border-radius: var(--radius-md);
  background: var(--accent-primary);
  color: var(--text-on-accent);
  padding: 0.75rem 1.1rem;
  font-weight: 600;
  cursor: pointer;
}

.primary-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.state-card {
  padding: 1.5rem;
  color: var(--text-secondary);
}

.state-card--error,
.form-error {
  color: var(--status-danger);
}

.form-success {
  margin-top: 1.25rem;
  color: var(--status-success);
}

@media (max-width: 700px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-field--full {
    grid-column: auto;
  }

  .provider-form-card {
    padding: 1rem;
  }
}
</style>
