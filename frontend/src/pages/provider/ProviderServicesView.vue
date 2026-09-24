<script setup lang="ts">
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';

import { useServicesStore } from '../../stores/services';

const servicesStore = useServicesStore();

async function toggleService(serviceId: number, isActive: boolean) {
  if (isActive) {
    await servicesStore.deactivate(serviceId);
  } else {
    await servicesStore.activate(serviceId);
  }
}

onMounted(() => {
  servicesStore.fetchServices();
});
</script>

<template>
  <section class="provider-page">
    <div class="page-header">
      <div>
        <p class="page-eyebrow">Provider</p>

        <h1 class="page-title">My services</h1>

        <p class="page-description">Create and manage the services you offer to customers.</p>
      </div>

      <RouterLink to="/provider/services/new" class="primary-button"> Add service </RouterLink>
    </div>

    <div v-if="servicesStore.loading" class="state-card">Loading services...</div>

    <div v-else-if="servicesStore.error" class="state-card state-card--error">
      {{ servicesStore.error }}
    </div>

    <div v-else-if="servicesStore.services.length === 0" class="empty-card">
      <div class="empty-icon">+</div>

      <h2>No services yet</h2>

      <p>Create your first service so customers can book it.</p>

      <RouterLink to="/provider/services/new" class="secondary-button"> Create service </RouterLink>
    </div>

    <div v-else class="services-grid">
      <article v-for="service in servicesStore.services" :key="service.id" class="service-card">
        <div class="service-card__header">
          <div>
            <h2>{{ service.name }}</h2>

            <span
              class="status-badge"
              :class="{
                'status-badge--active': service.is_active,
                'status-badge--inactive': !service.is_active,
              }"
            >
              {{ service.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>

        <p class="service-description">
          {{ service.description || 'No description provided.' }}
        </p>

        <div class="service-meta">
          <span> {{ service.duration_minutes }} min </span>

          <span> ₹{{ service.price }} </span>
        </div>

        <div class="service-actions">
          <RouterLink :to="`/provider/services/${service.id}`" class="secondary-button">
            Edit
          </RouterLink>

          <button
            class="text-button"
            type="button"
            :disabled="servicesStore.saving"
            @click="toggleService(service.id, service.is_active)"
          >
            {{ service.is_active ? 'Deactivate' : 'Activate' }}
          </button>
        </div>
      </article>
    </div>
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
}

.page-description {
  margin: 0.45rem 0 0;
  color: var(--text-secondary);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.service-card,
.empty-card,
.state-card {
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--surface-primary);
  box-shadow: var(--shadow-sm);
}

.service-card {
  display: flex;
  flex-direction: column;
  min-height: 240px;
  padding: 1.25rem;
}

.service-card__header {
  display: flex;
  justify-content: space-between;
}

.service-card h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.05rem;
}

.status-badge {
  display: inline-flex;
  margin-top: 0.6rem;
  border-radius: 999px;
  padding: 0.25rem 0.55rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge--active {
  background: var(--status-success-soft);
  color: var(--status-success);
}

.status-badge--inactive {
  background: var(--surface-tertiary);
  color: var(--text-secondary);
}

.service-description {
  flex: 1;
  margin: 1rem 0;
  color: var(--text-secondary);
  line-height: 1.6;
}

.service-meta {
  display: flex;
  gap: 1rem;
  color: var(--text-primary);
  font-weight: 600;
}

.service-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.primary-button,
.secondary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  padding: 0.7rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
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

.text-button {
  border: 0;
  background: transparent;
  color: var(--accent-primary);
  font-weight: 600;
  cursor: pointer;
}

.empty-card,
.state-card {
  padding: 2rem;
  text-align: center;
}

.empty-card h2 {
  margin: 0.75rem 0 0.35rem;
  color: var(--text-primary);
}

.empty-card p {
  margin: 0 0 1.25rem;
  color: var(--text-secondary);
}

.empty-icon {
  display: inline-flex;
  width: 2.5rem;
  height: 2.5rem;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--accent-primary-soft);
  color: var(--accent-primary);
  font-size: 1.25rem;
}

.state-card {
  color: var(--text-secondary);
}

.state-card--error {
  color: var(--status-danger);
}

@media (max-width: 700px) {
  .page-header {
    align-items: stretch;
    flex-direction: column;
  }

  .primary-button {
    width: 100%;
  }
}
</style>
