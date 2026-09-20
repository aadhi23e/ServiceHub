<script setup lang="ts">
import { computed } from "vue";

import {
  useThemeStore,
  type ThemeMode,
} from "../stores/theme";

const themeStore = useThemeStore();

const options: Array<{
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

const activeLabel = computed(() => {
  const activeOption = options.find(
    (option) => option.value === themeStore.mode,
  );

  return activeOption?.label ?? "System";
});

function selectTheme(mode: ThemeMode): void {
  themeStore.setTheme(mode);
}
</script>

<template>
  <div class="theme-toggle">
    <span class="theme-toggle__label">
      Theme
    </span>

    <div
      class="theme-toggle__options"
      role="group"
      aria-label="Theme selection"
    >
      <button
        v-for="option in options"
        :key="option.value"
        type="button"
        class="theme-toggle__option"
        :class="{
          'theme-toggle__option--active':
            themeStore.mode === option.value,
        }"
        :aria-label="`Use ${option.label} theme`"
        :aria-pressed="themeStore.mode === option.value"
        @click="selectTheme(option.value)"
      >
        <span aria-hidden="true">
          {{ option.icon }}
        </span>

        <span class="theme-toggle__option-label">
          {{ option.label }}
        </span>
      </button>
    </div>

    <span class="theme-toggle__current">
      {{ activeLabel }}
    </span>
  </div>
</template>

<style scoped>
.theme-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.theme-toggle__label {
  color: var(--color-text-muted);
  font-size: 0.8rem;
  font-weight: 600;
}

.theme-toggle__options {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 3px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface-secondary);
}

.theme-toggle__option {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 32px;
  padding: 0 10px;
  border: 0;
  border-radius: var(--radius-full);
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 0.78rem;
  font-weight: 600;
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast),
    box-shadow var(--transition-fast);
}

.theme-toggle__option:hover {
  color: var(--color-text-primary);
}

.theme-toggle__option--active {
  background: var(--color-surface);
  color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.theme-toggle__option:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.theme-toggle__option-label {
  white-space: nowrap;
}

.theme-toggle__current {
  display: none;
}

@media (max-width: 640px) {
  .theme-toggle__label {
    display: none;
  }

  .theme-toggle__option {
    width: 34px;
    padding: 0;
    justify-content: center;
  }

  .theme-toggle__option-label {
    display: none;
  }
}
</style>