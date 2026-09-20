<script setup lang="ts">
defineProps<{
  unreadCount?: number;
}>();
</script>

<template>
  <button
    type="button"
    class="notification-button"
    aria-label="Notifications"
  >
    <span
      class="notification-button__icon"
      aria-hidden="true"
    >
      ◉
    </span>

    <span
      v-if="unreadCount && unreadCount > 0"
      class="notification-button__badge"
    >
      {{ unreadCount > 9 ? "9+" : unreadCount }}
    </span>
  </button>
</template>

<style scoped>
.notification-button {
  position: relative;
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast),
    border-color var(--transition-fast);
}

.notification-button:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
  border-color: var(--color-border-strong);
}

.notification-button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.notification-button__icon {
  font-size: 1rem;
}

.notification-button__badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 17px;
  height: 17px;
  display: grid;
  place-items: center;
  padding: 0 4px;
  border: 2px solid var(--color-surface);
  border-radius: var(--radius-full);
  background: var(--color-danger);
  color: white;
  font-size: 0.62rem;
  font-weight: 700;
}
</style>