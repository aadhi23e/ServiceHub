<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="auth-layout">
    <aside class="auth-layout__brand">
      <div class="auth-layout__brand-content">
        <div class="auth-layout__logo">SH</div>

        <h1>ServiceHub</h1>

        <p>Find trusted services and manage your bookings in one place.</p>
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
  width: 100%;
  min-height: 100dvh;
  display: grid;
  grid-template-columns: 60% 40%;
  overflow: hidden;
  background: var(--color-background);
}

/* --------------------------------------------------
   BRAND SIDE
-------------------------------------------------- */

.auth-layout__brand {
  min-width: 0;
  display: flex;
  align-items: center;
  padding: var(--space-12);
  background: linear-gradient(135deg, var(--color-primary-800), var(--color-primary-600));
  color: var(--color-text-inverse);
}

.auth-layout__brand-content {
  width: 100%;
  max-width: 620px;
  margin: 0 auto;
}

.auth-layout__logo {
  width: 60px;
  height: 60px;

  display: grid;
  place-items: center;

  margin-bottom: var(--space-6);

  border-radius: var(--radius-lg);

  background: rgb(255 255 255 / 0.14);
  border: 1px solid rgb(255 255 255 / 0.2);

  font-size: 1.3rem;
  font-weight: 800;
}

.auth-layout__brand h1 {
  margin: 0 0 var(--space-4);

  font-size: clamp(2.25rem, 4vw, 4rem);
  line-height: 1.05;
  letter-spacing: -0.03em;
}

.auth-layout__brand p {
  max-width: 500px;

  margin: 0;

  color: rgb(255 255 255 / 0.82);

  font-size: 1.05rem;
  line-height: 1.7;
}

/* --------------------------------------------------
   FORM SIDE
-------------------------------------------------- */

.auth-layout__content {
  min-width: 0;
  min-height: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: clamp(var(--space-6), 4vw, var(--space-12));

  overflow-y: auto;

  background: var(--color-surface);
}

.auth-layout__container {
  width: 100%;
  max-width: 520px;
  margin: auto;
}

/* --------------------------------------------------
   TABLET
-------------------------------------------------- */

@media (max-width: 1000px) {
  .auth-layout {
    grid-template-columns: 55% 45%;
  }

  .auth-layout__brand {
    padding: var(--space-8);
  }

  .auth-layout__content {
    padding: var(--space-6);
  }

  .auth-layout__container {
    max-width: 480px;
  }
}

/* --------------------------------------------------
   MOBILE
-------------------------------------------------- */

@media (max-width: 800px) {
  .auth-layout {
    min-height: 100dvh;
    grid-template-columns: 1fr;
    overflow: auto;
  }

  .auth-layout__brand {
    min-height: 220px;
    padding: var(--space-8);
  }

  .auth-layout__brand-content {
    max-width: 600px;
    margin: 0;
  }

  .auth-layout__logo {
    width: 52px;
    height: 52px;
    margin-bottom: var(--space-4);
  }

  .auth-layout__brand h1 {
    margin-bottom: var(--space-3);
    font-size: 2.25rem;
  }

  .auth-layout__brand p {
    font-size: 0.95rem;
  }

  .auth-layout__content {
    min-height: auto;
    padding: var(--space-8) var(--space-5);
    overflow: visible;
  }

  .auth-layout__container {
    max-width: 560px;
  }
}
</style>
