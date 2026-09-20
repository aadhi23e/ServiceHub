<script setup lang="ts">
import { computed, ref } from "vue";

import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();

const open = ref(false);

const userName = computed(() => {
  if (!authStore.user) {
    return "User";
  }

  return `${authStore.user.first_name} ${authStore.user.last_name}`;
});

const userInitial = computed(() => {
  return authStore.user?.first_name?.charAt(0).toUpperCase() ?? "U";
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

function toggleMenu(): void {
  open.value = !open.value;
}

function closeMenu(): void {
  open.value = false;
}
</script>

<template>
  <div class="user-menu">
    <button
      type="button"
      class="user-menu__trigger"
      :aria-expanded="open"
      aria-haspopup="menu"
      @click="toggleMenu"
    >
      <span class="user-menu__avatar">
        {{ userInitial }}
      </span>

      <span class="user-menu__identity">
        <strong>{{ userName }}</strong>
        <small>{{ roleLabel }}</small>
      </span>

      <span class="user-menu__chevron">
        {{ open ? "⌃" : "⌄" }}
      </span>
    </button>

    <div
      v-if="open"
      class="user-menu__dropdown"
      role="menu"
    >
      <div class="user-menu__summary">
        <strong>{{ userName }}</strong>
        <span>{{ authStore.user?.email }}</span>
      </div>

      <div class="user-menu__divider" />

      <RouterLink
        :to="`/${authStore.role?.toLowerCase()}/profile`"
        class="user-menu__item"
        role="menuitem"
        @click="closeMenu"
      >
        Profile
      </RouterLink>

      <button
        type="button"
        class="user-menu__item"
        role="menuitem"
        @click="closeMenu"
      >
        Settings
      </button>

      <div class="user-menu__divider" />

      <button
        type="button"
        class="user-menu__item user-menu__item--danger"
        role="menuitem"
        @click="closeMenu"
      >
        Sign out
      </button>
    </div>
  </div>
</template>

<style scoped>
.user-menu {
  position: relative;
}

.user-menu__trigger {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 40px;
  padding: 3px 6px 3px 4px;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-primary);
  text-align: left;
}

.user-menu__trigger:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border);
}

.user-menu__trigger:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.user-menu__avatar {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: var(--radius-full);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 0.8rem;
  font-weight: 700;
}

.user-menu__identity {
  display: flex;
  flex-direction: column;
  min-width: 100px;
}

.user-menu__identity strong {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.8rem;
}

.user-menu__identity small {
  margin-top: 2px;
  color: var(--color-text-muted);
  font-size: 0.7rem;
}

.user-menu__chevron {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.user-menu__dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  z-index: 100;
  width: 230px;
  padding: var(--space-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-lg);
}

.user-menu__summary {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: var(--space-3);
}

.user-menu__summary strong {
  font-size: 0.85rem;
}

.user-menu__summary span {
  overflow: hidden;
  color: var(--color-text-muted);
  font-size: 0.72rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-menu__divider {
  height: 1px;
  margin: var(--space-2) 0;
  background: var(--color-border);
}

.user-menu__item {
  width: 100%;
  display: block;
  padding: 10px 12px;
  border: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 0.8rem;
  text-align: left;
}

.user-menu__item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.user-menu__item--danger {
  color: var(--color-danger);
}

@media (max-width: 640px) {
  .user-menu__identity,
  .user-menu__chevron {
    display: none;
  }

  .user-menu__trigger {
    padding: 0;
  }
}
</style>