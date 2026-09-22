<script setup lang="ts">
import { computed, ref } from "vue";
import { RouterView, useRoute } from "vue-router";

import AppSidebar from "../components/AppSidebar.vue";
import NotificationButton from "../components/NotificationButton.vue";
import ThemeToggle from "../components/ThemeToggle.vue";
import UserMenu from "../components/UserMenu.vue";

import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const route = useRoute();

const mobileSidebarOpen = ref(false);

const pageTitle = computed(() => {
  if (typeof route.meta.title === "string") {
    return route.meta.title;
  }

  switch (authStore.role) {
    case "CUSTOMER":
      return "Customer Dashboard";
    case "PROVIDER":
      return "Provider Dashboard";
    case "ADMIN":
      return "Admin Dashboard";
    default:
      return "Dashboard";
  }
});

const pageDescription = computed(() => {
  if (typeof route.meta.description === "string") {
    return route.meta.description;
  }

  return "Manage your ServiceHub activity.";
});

function toggleMobileSidebar(): void {
  mobileSidebarOpen.value = !mobileSidebarOpen.value;
}

function closeMobileSidebar(): void {
  mobileSidebarOpen.value = false;
}
</script>

<template>
  <div class="app-shell">
    <AppSidebar
      :mobile-open="mobileSidebarOpen"
      @close="closeMobileSidebar"
    />

    <div class="app-shell__main">
      <header class="app-topbar">
        <div class="app-topbar__left">
          <button
            type="button"
            class="mobile-menu-button"
            aria-label="Open navigation"
            @click="toggleMobileSidebar"
          >
            <span />
            <span />
            <span />
          </button>

          <div class="page-heading">
            <span class="page-heading__eyebrow">
              ServiceHub
            </span>

            <h1>{{ pageTitle }}</h1>

            <p>{{ pageDescription }}</p>
          </div>
        </div>

        <div class="app-topbar__actions">
          <ThemeToggle />

          <NotificationButton :unread-count="0" />

          <div class="topbar-divider" />

          <UserMenu />
        </div>
      </header>

      <main class="app-shell__content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: var(--color-background);
  color: var(--color-text-primary);
}

.app-shell__main {
  min-height: 100vh;
  margin-left: 260px;
}

.app-topbar {
  position: sticky;
  top: 0;
  z-index: 30;
  height: 76px;
  /* min-height: 76px; */
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-6);
  padding: var(--space-3) var(--space-8);
  background: color-mix(
    in srgb,
    var(--color-surface) 94%,
    transparent
  );
  border-bottom: 1px solid var(--color-border);
  backdrop-filter: blur(12px);
}

.app-topbar__left {
  display: flex;
  align-items: center;
  min-width: 0;
}

.page-heading {
  min-width: 0;
}

.page-heading__eyebrow {
  display: block;
  margin-bottom: 2px;
  color: var(--color-text-muted);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page-heading h1 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 1.15rem;
  line-height: 1.3;
}

.page-heading p {
  margin: 3px 0 0;
  color: var(--color-text-muted);
  font-size: 0.75rem;
}

.app-topbar__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}

.topbar-divider {
  width: 1px;
  height: 30px;
  background: var(--color-border);
}

.mobile-menu-button {
  display: none;
  width: 40px;
  height: 40px;
  margin-right: var(--space-3);
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 4px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
}

.mobile-menu-button span {
  width: 17px;
  height: 2px;
  border-radius: 2px;
  background: var(--color-text-secondary);
}

.mobile-menu-button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.app-shell__content {
  min-height: calc(100vh - 76px);
  padding: var(--space-6);
}

@media (max-width: 1100px) {
  .app-topbar {
    padding-left: var(--space-5);
    padding-right: var(--space-5);
  }

  .app-shell__content {
    padding: var(--space-4);
  }

  .app-topbar__actions {
    gap: var(--space-2);
  }
}

@media (max-width: 900px) {
  .app-shell__main {
    margin-left: 0;
  }

  .mobile-menu-button {
    display: flex;
  }
}

@media (max-width: 760px) {
  .page-heading p {
    display: none;
  }

  .topbar-divider {
    display: none;
  }
}

@media (max-width: 640px) {
  .app-topbar {
    min-height: 68px;
    padding: var(--space-3) var(--space-4);
  }

  .page-heading h1 {
    font-size: 1rem;
  }

  .page-heading__eyebrow {
    font-size: 0.6rem;
  }

  .app-shell__content {
    min-height: calc(100vh - 68px);
    padding: var(--space-2);
  }
}
</style>