import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';

export type ThemeMode = 'system' | 'light' | 'dark';

const STORAGE_KEY = 'servicehub-theme';

function getStoredTheme(): ThemeMode {
  const storedTheme = localStorage.getItem(STORAGE_KEY);

  if (storedTheme === 'system' || storedTheme === 'light' || storedTheme === 'dark') {
    return storedTheme;
  }

  return 'system';
}

function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export const useThemeStore = defineStore('theme', () => {
  const mode = ref<ThemeMode>(getStoredTheme());

  const resolvedTheme = ref<'light' | 'dark'>(
    mode.value === 'system' ? getSystemTheme() : mode.value
  );

  const isDark = computed(() => resolvedTheme.value === 'dark');

  function updateResolvedTheme(): void {
    resolvedTheme.value = mode.value === 'system' ? getSystemTheme() : mode.value;
  }

  function applyTheme(): void {
    document.documentElement.dataset.theme = resolvedTheme.value;
  }

  function setTheme(newMode: ThemeMode): void {
    mode.value = newMode;
    localStorage.setItem(STORAGE_KEY, newMode);

    updateResolvedTheme();
    applyTheme();
  }

  function initialize(): void {
    updateResolvedTheme();
    applyTheme();

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    mediaQuery.addEventListener('change', () => {
      if (mode.value === 'system') {
        updateResolvedTheme();
        applyTheme();
      }
    });
  }

  watch(resolvedTheme, applyTheme);

  return {
    mode,
    resolvedTheme,
    isDark,
    setTheme,
    initialize,
  };
});
