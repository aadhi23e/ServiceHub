<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";
import {
  useThemeStore,
  type ThemeMode,
} from "../stores/theme";

const authStore = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

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

const themeOptions: Array<{
  value: ThemeMode;
  label: string;
  icon: string;
}> = [
  {
    value: "system",
    label: "System",
    icon: "◐",
  },
  {
    value: "light",
    label: "Light",
    icon: "☀",
  },
  {
    value: "dark",
    label: "Dark",
    icon: "☾",
  },
];

const activeThemeLabel = computed(() => {
  return (
    themeOptions.find(
      (option) => option.value === themeStore.mode,
    )?.label ?? "System"
  );
});

function toggleMenu(): void {
  open.value = !open.value;
}

function closeMenu(): void {
  open.value = false;
}

function selectTheme(mode: ThemeMode): void {
  themeStore.setTheme(mode);
}

function openSettings(): void {
  closeMenu();
  router.push({ name: "settings" });
}

async function signout(): Promise<void> {
  try {
    await authStore.signout();
  } finally {
    open.value = false;
    await router.replace({ name: "login" });
  }
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

      <span
        class="user-menu__chevron"
        aria-hidden="true"
      >
        <svg
          viewBox="0 0 20 20"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="m5 7.5 5 5 5-5" />
        </svg>
      </span>
    </button>

    <div
      v-if="open"
      class="user-menu__dropdown"
      role="menu"
    >
      <!-- Account summary -->
      <div class="user-menu__summary">
        <div class="user-menu__summary-avatar">
          {{ userInitial }}
        </div>

        <div class="user-menu__summary-content">
          <strong>{{ userName }}</strong>
          <span>{{ authStore.user?.email }}</span>
        </div>
      </div>

      <div class="user-menu__divider" />

      <!-- Account actions -->
      <div class="user-menu__section">
        <RouterLink
          :to="`/${authStore.role?.toLowerCase()}/profile`"
          class="user-menu__item"
          role="menuitem"
          @click="closeMenu"
        >
          <span class="user-menu__item-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle cx="12" cy="8" r="3.5" />
              <path d="M5 20c.8-3.4 3.2-5.2 7-5.2s6.2 1.8 7 5.2" />
            </svg>
          </span>

          <span class="user-menu__item-content">
            <strong>Profile</strong>
            <small>Manage your profile</small>
          </span>
        </RouterLink>

        <button
          type="button"
          class="user-menu__item"
          role="menuitem"
          @click="openSettings"
        >
          <span class="user-menu__item-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M12 15.2a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4Z"
              />
              <path
                d="m19.4 15 .1.1a2 2 0 0 1-2.8 2.8l-.1-.1a1.8 1.8 0 0 0-3 .9v.2a2 2 0 0 1-4 0v-.2a1.8 1.8 0 0 0-3-.9l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.8 1.8 0 0 0-.9-3H2.8a2 2 0 0 1 0-4H3a1.8 1.8 0 0 0 .9-3l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.8 1.8 0 0 0 3-.9V2.8a2 2 0 0 1 4 0V3a1.8 1.8 0 0 0 3 .9l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.8 1.8 0 0 0 .9 3h.2a2 2 0 0 1 0 4h-.2a1.8 1.8 0 0 0-.9 1.3Z"
              />
            </svg>
          </span>

          <span class="user-menu__item-content">
            <strong>Settings</strong>
            <small>Preferences and appearance</small>
          </span>
        </button>
      </div>

      <div class="user-menu__divider" />

      <!-- Appearance -->
      <div class="user-menu__section">
        <div class="user-menu__section-heading">
          <span>Appearance</span>
          <small>{{ activeThemeLabel }}</small>
        </div>

        <div
          class="user-menu__theme-options"
          role="group"
          aria-label="Theme selection"
        >
          <button
            v-for="option in themeOptions"
            :key="option.value"
            type="button"
            class="user-menu__theme-option"
            :class="{
              'user-menu__theme-option--active':
                themeStore.mode === option.value,
            }"
            :aria-label="`Use ${option.label} theme`"
            :aria-pressed="themeStore.mode === option.value"
            @click="selectTheme(option.value)"
          >
            <span
              class="user-menu__theme-icon"
              aria-hidden="true"
            >
              {{ option.icon }}
            </span>

            <span>{{ option.label }}</span>
          </button>
        </div>
      </div>

      <div class="user-menu__divider" />

      <!-- Sign out -->
      <button
        type="button"
        class="user-menu__item user-menu__item--danger"
        role="menuitem"
        @click="signout"
      >
        <span class="user-menu__item-icon">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M10 17l5-5-5-5" />
            <path d="M15 12H3" />
            <path d="M21 19V5a2 2 0 0 0-2-2h-5" />
          </svg>
        </span>

        <span class="user-menu__item-content">
          <strong>Sign out</strong>
          <small>End your current session</small>
        </span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.user-menu {
  position: relative;
  flex-shrink: 0;
}

.user-menu__trigger {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 44px;
  padding: 4px 8px 4px 5px;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-primary);
  text-align: left;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast);
}

.user-menu__trigger:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border);
}

.user-menu__trigger:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.user-menu__avatar,
.user-menu__summary-avatar {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: var(--radius-full);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-weight: 800;
}

.user-menu__avatar {
  width: 34px;
  height: 34px;
  font-size: 0.78rem;
}

.user-menu__identity {
  display: flex;
  flex-direction: column;
  min-width: 0;
  width: 112px;
}

.user-menu__identity strong {
  overflow: hidden;
  font-size: 0.78rem;
  font-weight: 700;
  line-height: 1.3;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-menu__identity small {
  margin-top: 2px;
  color: var(--color-text-muted);
  font-size: 0.68rem;
  line-height: 1.2;
}

.user-menu__chevron {
  width: 16px;
  height: 16px;
  display: grid;
  place-items: center;
  color: var(--color-text-muted);
}

.user-menu__chevron svg {
  width: 14px;
  height: 14px;
}

.user-menu__dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  z-index: 100;
  width: 310px;
  padding: 8px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-lg);
}

.user-menu__summary {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
}

.user-menu__summary-avatar {
  width: 42px;
  height: 42px;
  font-size: 0.9rem;
}

.user-menu__summary-content {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.user-menu__summary-content strong {
  overflow: hidden;
  color: var(--color-text-primary);
  font-size: 0.82rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-menu__summary-content span {
  overflow: hidden;
  color: var(--color-text-muted);
  font-size: 0.7rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-menu__divider {
  height: 1px;
  margin: 6px 4px;
  background: var(--color-border);
}

.user-menu__section {
  padding: 3px 0;
}

.user-menu__item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 11px;
  min-height: 46px;
  padding: 7px 9px;
  border: 0;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-secondary);
  text-align: left;
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast);
}

.user-menu__item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.user-menu__item:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
}

.user-menu__item-icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
}

.user-menu__item-icon svg {
  width: 17px;
  height: 17px;
}

.user-menu__item-content {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-menu__item-content strong {
  color: inherit;
  font-size: 0.76rem;
  font-weight: 650;
  line-height: 1.3;
}

.user-menu__item-content small {
  color: var(--color-text-muted);
  font-size: 0.66rem;
  line-height: 1.3;
}

.user-menu__section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 9px 8px;
}

.user-menu__section-heading span {
  color: var(--color-text-primary);
  font-size: 0.72rem;
  font-weight: 700;
}

.user-menu__section-heading small {
  color: var(--color-text-muted);
  font-size: 0.65rem;
}

.user-menu__theme-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5px;
  padding: 0 2px;
}

.user-menu__theme-option {
  min-width: 0;
  min-height: 54px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 6px;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);
  color: var(--color-text-muted);
  font-size: 0.64rem;
  font-weight: 650;
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast),
    border-color var(--transition-fast),
    box-shadow var(--transition-fast);
}

.user-menu__theme-option:hover {
  border-color: var(--color-border);
  color: var(--color-text-primary);
}

.user-menu__theme-option--active {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.user-menu__theme-icon {
  font-size: 0.95rem;
  line-height: 1;
}

.user-menu__item--danger {
  color: var(--color-danger);
}

.user-menu__item--danger .user-menu__item-icon {
  color: var(--color-danger);
}

@media (max-width: 640px) {
  .user-menu__identity,
  .user-menu__chevron {
    display: none;
  }

  .user-menu__trigger {
    padding: 3px;
  }

  .user-menu__dropdown {
    width: min(310px, calc(100vw - 24px));
    right: -4px;
  }
}
</style>