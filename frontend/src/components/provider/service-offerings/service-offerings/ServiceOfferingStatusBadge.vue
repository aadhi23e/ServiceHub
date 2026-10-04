<script setup lang="ts">
defineProps<{
  active: boolean;
}>();
</script>

<template>
  <span
    class="inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium"
    :class="
      active
        ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
        : 'border-slate-200 bg-slate-50 text-slate-600'
    "
  >
    {{ active ? "Active" : "Inactive" }}
  </span>
</template>