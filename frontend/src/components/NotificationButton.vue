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
    title="Notifications"
  >
    <span
      class="notification-button__icon"
      aria-hidden="true"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path
          d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"
        />
        <path d="M10 21h4" />
      </svg>
    </span>

    <span
      v-if="unreadCount && unreadCount > 0"
      class="notification-button__badge"
      aria-hidden="true"
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
  flex-shrink: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast),
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    transform var(--transition-fast);
}

.notification-button:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}

.notification-button:active {
  transform: translateY(1px);
}

.notification-button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.notification-button__icon {
  width: 19px;
  height: 19px;
  display: grid;
  place-items: center;
}

.notification-button__icon svg {
  width: 100%;
  height: 100%;
}

.notification-button__badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 18px;
  height: 18px;
  display: grid;
  place-items: center;
  padding: 0 4px;
  border: 2px solid var(--color-surface);
  border-radius: var(--radius-full);
  background: var(--color-danger);
  color: var(--color-text-inverse);
  font-size: 0.6rem;
  font-weight: 800;
  line-height: 1;
}
</style>