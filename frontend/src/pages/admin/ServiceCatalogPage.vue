<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import {
  type ServiceCategory,
  type Service,
  listServiceCategories,
  listServices,
} from "../../api/serviceCatalog";

import CategoryList from "../../components/admin/service-catalog/CategoryList.vue";
import CategoryForm from "../../components/admin/service-catalog/CategoryForm.vue";
import ServiceList from "../../components/admin/service-catalog/ServiceList.vue";
import ServiceForm from "../../components/admin/service-catalog/ServiceForm.vue";

type CatalogTab = "categories" | "services";

const activeTab = ref<CatalogTab>("categories");

const categories = ref<ServiceCategory[]>([]);
const services = ref<Service[]>([]);

const loading = ref(true);
const errorMessage = ref("");

const showCategoryForm = ref(false);
const showServiceForm = ref(false);

const editingCategory = ref<ServiceCategory | null>(null);
const editingService = ref<Service | null>(null);

const activeCategoryCount = computed(
  () => categories.value.filter((category) => category.is_active).length,
);

const activeServiceCount = computed(
  () => services.value.filter((service) => service.is_active).length,
);

async function loadCatalog() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const [categoryData, serviceData] = await Promise.all([
      listServiceCategories(),
      listServices(),
    ]);

    categories.value = categoryData;
    services.value = serviceData;
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Unable to load service catalog.";
  } finally {
    loading.value = false;
  }
}

function openCreateCategory() {
  editingCategory.value = null;
  showCategoryForm.value = true;
}

function openEditCategory(category: ServiceCategory) {
  editingCategory.value = category;
  showCategoryForm.value = true;
}

function closeCategoryForm() {
  showCategoryForm.value = false;
  editingCategory.value = null;
}

function openCreateService() {
  editingService.value = null;
  showServiceForm.value = true;
}

function openEditService(service: Service) {
  editingService.value = service;
  showServiceForm.value = true;
}

function closeServiceForm() {
  showServiceForm.value = false;
  editingService.value = null;
}

async function handleCategorySaved() {
  closeCategoryForm();
  await loadCatalog();
}

async function handleServiceSaved() {
  closeServiceForm();
  await loadCatalog();
}

function handleCategoryServices(categoryId: string) {
  activeTab.value = "services";
}

onMounted(loadCatalog);
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <section class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <p class="page-eyebrow">
          Administration
        </p>

        <h1 class="page-title">
          Service Catalog
        </h1>

        <p class="page-description">
          Manage the services customers can discover and book on ServiceHub.
        </p>
      </div>

      <div class="flex flex-wrap gap-3">
        <button
          v-if="activeTab === 'categories'"
          type="button"
          class="btn-primary"
          @click="openCreateCategory"
        >
          <span>+</span>
          Add category
        </button>

        <button
          v-else
          type="button"
          class="btn-primary"
          @click="openCreateService"
        >
          <span>+</span>
          Add service
        </button>
      </div>
    </section>

    <!-- Summary -->
    <section class="grid gap-4 sm:grid-cols-2">
      <article class="surface-card p-5">
        <div class="flex items-start justify-between">
          <div>
            <p class="metric-label">Categories</p>
            <p class="metric-value">
              {{ categories.length }}
            </p>
          </div>

          <div class="metric-icon">
            C
          </div>
        </div>

        <p class="metric-description">
          {{ activeCategoryCount }} active categories
        </p>
      </article>

      <article class="surface-card p-5">
        <div class="flex items-start justify-between">
          <div>
            <p class="metric-label">Services</p>
            <p class="metric-value">
              {{ services.length }}
            </p>
          </div>

          <div class="metric-icon">
            S
          </div>
        </div>

        <p class="metric-description">
          {{ activeServiceCount }} active services
        </p>
      </article>
    </section>

    <!-- Error -->
    <div
      v-if="errorMessage"
      class="alert-error"
      role="alert"
    >
      <div>
        <p class="font-semibold">Unable to load catalog</p>
        <p class="mt-1 text-sm">
          {{ errorMessage }}
        </p>
      </div>

      <button
        type="button"
        class="btn-secondary"
        @click="loadCatalog"
      >
        Retry
      </button>
    </div>

    <!-- Tabs -->
    <section class="surface-card overflow-hidden">
      <div class="border-b border-[var(--border-subtle)] px-4 sm:px-6">
        <nav class="flex gap-6">
          <button
            type="button"
            class="catalog-tab"
            :class="{ 'catalog-tab-active': activeTab === 'categories' }"
            @click="activeTab = 'categories'"
          >
            Categories
            <span class="catalog-tab-count">
              {{ categories.length }}
            </span>
          </button>

          <button
            type="button"
            class="catalog-tab"
            :class="{ 'catalog-tab-active': activeTab === 'services' }"
            @click="activeTab = 'services'"
          >
            Services
            <span class="catalog-tab-count">
              {{ services.length }}
            </span>
          </button>
        </nav>
      </div>

      <div class="p-4 sm:p-6">
        <div
          v-if="loading"
          class="py-16 text-center"
        >
          <div class="loading-spinner mx-auto" />
          <p class="mt-4 text-sm text-[var(--text-secondary)]">
            Loading service catalog...
          </p>
        </div>

        <CategoryList
          v-else-if="activeTab === 'categories'"
          :categories="categories"
          :services="services"
          @edit="openEditCategory"
          @view-services="handleCategoryServices"
          @changed="loadCatalog"
        />

        <ServiceList
          v-else
          :services="services"
          :categories="categories"
          @edit="openEditService"
          @changed="loadCatalog"
        />
      </div>
    </section>

    <!-- Category modal -->
    <CategoryForm
      v-if="showCategoryForm"
      :category="editingCategory"
      @close="closeCategoryForm"
      @saved="handleCategorySaved"
    />

    <!-- Service modal -->
    <ServiceForm
      v-if="showServiceForm"
      :service="editingService"
      :categories="categories"
      @close="closeServiceForm"
      @saved="handleServiceSaved"
    />
  </div>
</template>
<style scoped>
/* =========================================================
   Page Header
   ========================================================= */

.page-eyebrow {
  color: var(--color-primary);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  line-height: 1rem;
  text-transform: uppercase;
}

.page-title {
  margin-top: var(--space-1);
  color: var(--color-text-primary);
  font-size: 1.875rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.25;
}

.page-description {
  margin-top: var(--space-2);
  color: var(--color-text-secondary);
  font-size: 0.9375rem;
  line-height: 1.5;
}


/* =========================================================
   Surface Card
   ========================================================= */

.surface-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}


/* =========================================================
   Buttons
   ========================================================= */

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);

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

.btn-primary:hover {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}

.btn-primary:active {
  background: var(--color-primary-active);
  border-color: var(--color-primary-active);
  transform: translateY(1px);
}

.btn-secondary {
  border: 1px solid var(--color-border-strong);
  background: var(--color-surface);
  color: var(--color-text-primary);
}

.btn-secondary:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border-strong);
}

.btn-primary:focus-visible,
.btn-secondary:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}


/* =========================================================
   Metric Cards
   ========================================================= */

.metric-label {
  color: var(--color-text-secondary);
  font-size: 0.8125rem;
  font-weight: 600;
  line-height: 1.25;
}

.metric-value {
  margin-top: var(--space-2);
  color: var(--color-text-primary);
  font-size: 1.875rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1;
}

.metric-description {
  margin-top: var(--space-3);
  color: var(--color-text-muted);
  font-size: 0.8125rem;
  line-height: 1.25;
}

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 40px;
  height: 40px;

  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);

  background: var(--color-primary-soft);
  color: var(--color-primary);

  font-size: 0.875rem;
  font-weight: 700;
}


/* =========================================================
   Error Alert
   ========================================================= */

.alert-error {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);

  padding: var(--space-4);

  border: 1px solid color-mix(
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

  color: var(--color-text-primary);
}


/* =========================================================
   Catalog Tabs
   ========================================================= */

.catalog-tab {
  position: relative;

  display: inline-flex;
  align-items: center;
  gap: var(--space-2);

  min-height: 56px;

  border: 0;
  border-bottom: 2px solid transparent;

  background: transparent;

  color: var(--color-text-secondary);

  font-size: 0.875rem;
  font-weight: 600;

  transition:
    color var(--transition-fast),
    border-color var(--transition-fast);
}

.catalog-tab:hover {
  color: var(--color-text-primary);
}

.catalog-tab-active {
  border-bottom-color: var(--color-primary);
  color: var(--color-primary);
}

.catalog-tab:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
}

.catalog-tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-width: 24px;
  height: 22px;
  padding: 0 var(--space-2);

  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);

  background: var(--color-surface-secondary);

  color: var(--color-text-muted);

  font-size: 0.6875rem;
  font-weight: 700;
  line-height: 1;
}

.catalog-tab-active .catalog-tab-count {
  border-color: var(--color-primary-200);
  background: var(--color-primary-soft);
  color: var(--color-primary);
}


/* =========================================================
   Loading
   ========================================================= */

.loading-spinner {
  width: 32px;
  height: 32px;

  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);

  border-radius: var(--radius-full);

  animation: catalog-spin 700ms linear infinite;
}

@keyframes catalog-spin {
  to {
    transform: rotate(360deg);
  }
}


/* =========================================================
   Responsive
   ========================================================= */

@media (max-width: 640px) {
  .page-title {
    font-size: 1.625rem;
  }

  .alert-error {
    flex-direction: column;
  }

  .alert-error .btn-secondary {
    width: 100%;
  }

  .catalog-tab {
    min-height: 52px;
  }
}
</style>