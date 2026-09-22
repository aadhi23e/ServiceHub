<script setup lang="ts">
import { computed } from "vue";

import {
  useThemeStore,
  type ThemeMode,
} from "../../stores/theme";

const themeStore = useThemeStore();

const themeOptions: Array<{
  value: ThemeMode;
  label: string;
  description: string;
  icon: string;
}> = [
  {
    value: "system",
    label: "System",
    description: "Follow your operating system preference.",
    icon: "◐",
  },
  {
    value: "light",
    label: "Light",
    description: "Use the light ServiceHub interface.",
    icon: "☀",
  },
  {
    value: "dark",
    label: "Dark",
    description: "Use the dark ServiceHub interface.",
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

function selectTheme(mode: ThemeMode): void {
  themeStore.setTheme(mode);
}
</script>

<template>
  <section class="settings-page">
    <header class="settings-page__header">
      <div>
        <span class="settings-page__eyebrow">
          Preferences
        </span>

        <h2>Settings</h2>

        <p>
          Manage your ServiceHub preferences and application experience.
        </p>
      </div>
    </header>

    <div class="settings-layout">
      <!-- Settings navigation -->
      <aside class="settings-sidebar">
        <nav
          class="settings-nav"
          aria-label="Settings sections"
        >
          <a
            href="#appearance"
            class="settings-nav__item settings-nav__item--active"
          >
            <span class="settings-nav__icon">
              ☼
            </span>

            <span>
              <strong>Appearance</strong>
              <small>Theme and display</small>
            </span>
          </a>

          <a
            href="#account"
            class="settings-nav__item"
          >
            <span class="settings-nav__icon">
              ◎
            </span>

            <span>
              <strong>Account</strong>
              <small>Account preferences</small>
            </span>
          </a>

          <a
            href="#notifications"
            class="settings-nav__item"
          >
            <span class="settings-nav__icon">
              ◉
            </span>

            <span>
              <strong>Notifications</strong>
              <small>Notification preferences</small>
            </span>
          </a>
        </nav>
      </aside>

      <!-- Settings content -->
      <div class="settings-content">
        <!-- Appearance -->
        <section
          id="appearance"
          class="settings-card"
        >
          <div class="settings-card__header">
            <div class="settings-card__icon">
              ☼
            </div>

            <div>
              <h3>Appearance</h3>
              <p>
                Customize how ServiceHub looks on your device.
              </p>
            </div>
          </div>

          <div class="settings-card__body">
            <div class="settings-row">
              <div class="settings-row__content">
                <strong>Theme</strong>

                <span>
                  Current theme: {{ activeThemeLabel }}
                </span>
              </div>
            </div>

            <div
              class="theme-grid"
              role="radiogroup"
              aria-label="Theme selection"
            >
              <button
                v-for="option in themeOptions"
                :key="option.value"
                type="button"
                class="theme-card"
                :class="{
                  'theme-card--active':
                    themeStore.mode === option.value,
                }"
                :aria-checked="themeStore.mode === option.value"
                role="radio"
                @click="selectTheme(option.value)"
              >
                <span class="theme-card__icon">
                  {{ option.icon }}
                </span>

                <span class="theme-card__content">
                  <strong>{{ option.label }}</strong>

                  <small>
                    {{ option.description }}
                  </small>
                </span>

                <span
                  class="theme-card__check"
                  aria-hidden="true"
                >
                  <svg
                    v-if="themeStore.mode === option.value"
                    viewBox="0 0 20 20"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="m4 10 4 4 8-8" />
                  </svg>
                </span>
              </button>
            </div>
          </div>
        </section>

        <!-- Account -->
        <section
          id="account"
          class="settings-card"
        >
          <div class="settings-card__header">
            <div class="settings-card__icon">
              ◎
            </div>

            <div>
              <h3>Account</h3>
              <p>
                Manage your account preferences.
              </p>
            </div>
          </div>

          <div class="settings-card__body">
            <div class="settings-row settings-row--disabled">
              <div class="settings-row__content">
                <strong>Account preferences</strong>
                <span>
                  More account settings will be available here.
                </span>
              </div>

              <span class="settings-row__status">
                Coming soon
              </span>
            </div>
          </div>
        </section>

        <!-- Notifications -->
        <section
          id="notifications"
          class="settings-card"
        >
          <div class="settings-card__header">
            <div class="settings-card__icon">
              ◉
            </div>

            <div>
              <h3>Notifications</h3>
              <p>
                Control how ServiceHub keeps you informed.
              </p>
            </div>
          </div>

          <div class="settings-card__body">
            <div class="settings-row settings-row--disabled">
              <div class="settings-row__content">
                <strong>Notification preferences</strong>
                <span>
                  Notification controls will be available here.
                </span>
              </div>

              <span class="settings-row__status">
                Coming soon
              </span>
            </div>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>

<style scoped>
.settings-page {
  width: min(1180px, 100%);
  margin: 0 auto;
}

.settings-page__header {
  margin-bottom: var(--space-7);
}

.settings-page__eyebrow {
  display: block;
  margin-bottom: 6px;
  color: var(--color-primary);
  font-size: 0.68rem;
  font-weight: 750;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.settings-page__header h2 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: clamp(1.5rem, 2vw, 1.9rem);
  line-height: 1.2;
  letter-spacing: -0.025em;
}

.settings-page__header p {
  max-width: 620px;
  margin: 8px 0 0;
  color: var(--color-text-secondary);
  font-size: 0.85rem;
  line-height: 1.6;
}

.settings-layout {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  align-items: start;
  gap: var(--space-7);
}

.settings-sidebar {
  position: sticky;
  top: 100px;
}

.settings-nav {
  display: grid;
  gap: 4px;
}

.settings-nav__item {
  display: flex;
  align-items: center;
  gap: 11px;
  min-height: 54px;
  padding: 8px 10px;
  border: 1px solid transparent;
  border-radius: var(--radius-md) 0 0 var(--radius-md);
  color: var(--color-text-secondary);
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast),
    border-color var(--transition-fast);
}

.settings-nav__item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.settings-nav__item--active {
  border-color: var(--color-border);
  background: var(--color-surface);
  color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.settings-nav__icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  background: var(--color-surface-secondary);
  font-size: 0.95rem;
}

.settings-nav__item--active .settings-nav__icon {
  background: var(--color-primary-soft);
}

.settings-nav__item > span:last-child {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.settings-nav__item strong {
  font-size: 0.74rem;
  font-weight: 700;
}

.settings-nav__item small {
  color: var(--color-text-muted);
  font-size: 0.65rem;
}

.settings-content {
  min-width: 0;
  display: grid;
  gap: var(--space-5);
}

.settings-card {
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}

.settings-card__header {
  display: flex;
  align-items: flex-start;
  gap: 13px;
  padding: 20px 22px;
  border-bottom: 1px solid var(--color-border);
}

.settings-card__icon {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 1rem;
}

.settings-card__header h3 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 0.9rem;
  font-weight: 750;
}

.settings-card__header p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
  font-size: 0.72rem;
  line-height: 1.5;
}

.settings-card__body {
  padding: 20px 22px;
}

.settings-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}

.settings-row__content {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.settings-row__content strong {
  color: var(--color-text-primary);
  font-size: 0.78rem;
  font-weight: 700;
}

.settings-row__content span {
  color: var(--color-text-muted);
  font-size: 0.7rem;
  line-height: 1.5;
}

.settings-row__status {
  flex-shrink: 0;
  padding: 5px 8px;
  border-radius: var(--radius-full);
  background: var(--color-surface-secondary);
  color: var(--color-text-muted);
  font-size: 0.62rem;
  font-weight: 650;
}

.settings-row--disabled {
  opacity: 0.75;
}

.theme-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.theme-card {
  position: relative;
  min-width: 0;
  min-height: 112px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  text-align: left;
  transition:
    border-color var(--transition-fast),
    background-color var(--transition-fast),
    box-shadow var(--transition-fast),
    transform var(--transition-fast);
}

.theme-card:hover {
  border-color: var(--color-border-strong);
  background: var(--color-surface-hover);
  transform: translateY(-1px);
}

.theme-card:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.theme-card--active {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.theme-card__icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-size: 1rem;
}

.theme-card__content {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.theme-card__content strong {
  color: var(--color-text-primary);
  font-size: 0.76rem;
  font-weight: 700;
}

.theme-card__content small {
  color: var(--color-text-muted);
  font-size: 0.66rem;
  line-height: 1.45;
}

.theme-card__check {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 20px;
  height: 20px;
  display: grid;
  place-items: center;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

.theme-card__check svg {
  width: 12px;
  height: 12px;
}

@media (max-width: 900px) {
  .settings-layout {
    grid-template-columns: 1fr;
    gap: var(--space-5);
  }

  .settings-sidebar {
    position: static;
  }

  .settings-nav {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .settings-page__header {
    margin-bottom: var(--space-5);
  }

  .settings-nav {
    grid-template-columns: 1fr;
  }

  .settings-card__header,
  .settings-card__body {
    padding: 16px;
  }

  .theme-grid {
    grid-template-columns: 1fr;
  }

  .theme-card {
    min-height: 88px;
    flex-direction: row;
    align-items: center;
  }

  .theme-card__content {
    padding-right: 24px;
  }
}
</style>