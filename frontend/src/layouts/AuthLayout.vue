<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <div class="auth-layout">
    <aside class="auth-layout__brand">
      <div class="auth-layout__brand-content">
        <div class="auth-layout__logo">
          SH
        </div>

        <h1>ServiceHub</h1>

        <p>
          Find trusted services and manage your bookings in one place.
        </p>
      </div>
    </aside>

    <main class="auth-layout__content">
      <div class="auth-layout__container">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(420px, 520px);
  background: var(--color-background);
}

.auth-layout__brand {
  display: flex;
  align-items: center;
  padding: var(--space-12);
  background:
    linear-gradient(
      135deg,
      var(--color-primary-800),
      var(--color-primary-600)
    );
  color: var(--color-text-inverse);
}

.auth-layout__brand-content {
  max-width: 520px;
  margin: 0 auto;
}

.auth-layout__logo {
  width: 56px;
  height: 56px;
  display: grid;
  place-items: center;
  margin-bottom: var(--space-6);
  border-radius: var(--radius-lg);
  background: rgb(255 255 255 / 0.14);
  border: 1px solid rgb(255 255 255 / 0.2);
  font-size: 1.25rem;
  font-weight: 800;
}

.auth-layout__brand h1 {
  margin: 0 0 var(--space-4);
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 1.1;
}

.auth-layout__brand p {
  margin: 0;
  max-width: 440px;
  color: rgb(255 255 255 / 0.82);
  font-size: 1.05rem;
  line-height: 1.7;
}

.auth-layout__content {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  background: var(--color-surface);
}

.auth-layout__container {
  width: 100%;
  max-width: 420px;
}

@media (max-width: 800px) {
  .auth-layout {
    grid-template-columns: 1fr;
  }

  .auth-layout__brand {
    min-height: 260px;
    padding: var(--space-8);
  }

  .auth-layout__brand-content {
    margin: 0;
  }

  .auth-layout__brand h1 {
    font-size: 2rem;
  }

  .auth-layout__content {
    padding: var(--space-6);
  }
}
</style>