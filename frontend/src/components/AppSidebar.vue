<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRoute } from "vue-router";

import { useAuthStore } from "../stores/auth";

interface NavigationItem {
  label: string;
  to: string;
  icon: string;
}

const props = defineProps<{
  mobileOpen: boolean;
}>();

const emit = defineEmits<{
  close: [];
}>();

const authStore = useAuthStore();
const route = useRoute();

const navigation = computed<NavigationItem[]>(() => {
  switch (authStore.role) {
    case "CUSTOMER":
      return [
        {
          label: "Dashboard",
          to: "/customer",
          icon: "⌂",
        },
        {
          label: "Find Services",
          to: "/customer/services",
          icon: "⌕",
        },
        {
          label: "My Bookings",
          to: "/customer/bookings",
          icon: "▣",
        },
        {
          label: "Notifications",
          to: "/customer/notifications",
          icon: "◉",
        },
        {
          label: "Profile",
          to: "/customer/profile",
          icon: "◎",
        },
      ];

    case "PROVIDER":
      return [
        {
          label: "Dashboard",
          to: "/provider",
          icon: "⌂",
        },
        {
          label: "My Services",
          to: "/provider/services",
          icon: "◇",
        },
        {
          label: "Availability",
          to: "/provider/availability",
          icon: "◷",
        },
        {
          label: "Bookings",
          to: "/provider/bookings",
          icon: "▣",
        },
        {
          label: "Notifications",
          to: "/provider/notifications",
          icon: "◉",
        },
        {
          label: "Profile",
          to: "/provider/profile",
          icon: "◎",
        },
      ];

    case "ADMIN":
      return [
        {
          label: "Dashboard",
          to: "/admin",
          icon: "⌂",
        },
        {
          label: "Users",
          to: "/admin/users",
          icon: "◎",
        },
        {
          label: "Providers",
          to: "/admin/providers",
          icon: "◇",
        },
        {
          label: "Bookings",
          to: "/admin/bookings",
          icon: "▣",
        },
        {
          label: "Categories",
          to: "/admin/categories",
          icon: "▦",
        },
        {
          label: "Audit Logs",
          to: "/admin/audit-logs",
          icon: "≡",
        },
      ];

    default:
      return [];
  }
});

const roleLabel = computed(() => {
  switch (authStore.role) {
    case "CUSTOMER":
      return "Customer";
    case "PROVIDER":
      return "Provider";
    case "ADMIN":
      return "Administrator";
    default:
      return "User";
  }
});

function isActive(item: NavigationItem): boolean {
  if (item.to === "/customer" || item.to === "/provider" || item.to === "/admin") {
    return route.path === item.to;
  }

  return route.path.startsWith(item.to);
}

function closeMobileSidebar(): void {
  emit("close");
}
</script>

<template>
  <div
    v-if="props.mobileOpen"
    class="sidebar-backdrop"
    @click="closeMobileSidebar"
  />

  <aside
    class="app-sidebar"
    :class="{ 'app-sidebar--mobile-open': props.mobileOpen }"
  >
    <div class="app-sidebar__header">
      <RouterLink
        to="/"
        class="app-brand"
        @click="closeMobileSidebar"
      >
        <span class="app-brand__logo">SH</span>

        <span class="app-brand__text">
          <strong>ServiceHub</strong>
          <small>{{ roleLabel }}</small>
        </span>
      </RouterLink>

      <button
        type="button"
        class="sidebar-close"
        aria-label="Close navigation"
        @click="closeMobileSidebar"
      >
        ×
      </button>
    </div>

    <nav
      class="app-sidebar__navigation"
      aria-label="Main navigation"
    >
      <RouterLink
        v-for="item in navigation"
        :key="item.to"
        :to="item.to"
        class="sidebar-item"
        :class="{
          'sidebar-item--active': isActive(item),
        }"
        @click="closeMobileSidebar"
      >
        <span
          class="sidebar-item__icon"
          aria-hidden="true"
        >
          {{ item.icon }}
        </span>

        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="app-sidebar__footer">
      <div class="sidebar-status">
        <span class="sidebar-status__dot" />
        <span>ServiceHub</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.app-sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 50;
  width: 260px;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
}

.app-sidebar__header {
  display: flex;
  align-items: center;
  min-height: 76px;
  padding: 0 var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.app-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-width: 0;
}

.app-brand__logo {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: white;
  font-size: 0.85rem;
  font-weight: 800;
}

.app-brand__text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-brand__text strong {
  color: var(--color-text-primary);
  font-size: 0.95rem;
}

.app-brand__text small {
  margin-top: 2px;
  color: var(--color-text-muted);
  font-size: 0.7rem;
}

.sidebar-close {
  display: none;
  margin-left: auto;
  border: 0;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 1.5rem;
}

.app-sidebar__navigation {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-5) var(--space-3);
  overflow-y: auto;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 44px;
  padding: 0 var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast);
}

.sidebar-item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.sidebar-item--active {
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-weight: 600;
}

.sidebar-item__icon {
  width: 22px;
  text-align: center;
  font-size: 1rem;
}

.app-sidebar__footer {
  margin-top: auto;
  padding: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.sidebar-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text-muted);
  font-size: 0.75rem;
}

.sidebar-status__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--color-success);
}

.sidebar-backdrop {
  display: none;
}

@media (max-width: 900px) {
  .app-sidebar {
    transform: translateX(-100%);
    transition: transform 200ms ease;
    box-shadow: var(--shadow-lg);
  }

  .app-sidebar--mobile-open {
    transform: translateX(0);
  }

  .sidebar-close {
    display: block;
  }

  .sidebar-backdrop {
    position: fixed;
    inset: 0;
    z-index: 40;
    display: block;
    background: rgb(0 0 0 / 0.45);
  }
}
</style>