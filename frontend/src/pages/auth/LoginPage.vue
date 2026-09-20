<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import { login } from "../../api/auth";
import { ApiError } from "../../api/client";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const email = ref("");
const password = ref("");

const isSubmitting = ref(false);
const errorMessage = ref("");
const showPassword = ref(false);

const canSubmit = computed(() => {
  return (
    email.value.trim().length > 0 &&
    password.value.length > 0 &&
    !isSubmitting.value
  );
});

function getDashboardRoute(role: string) {
  switch (role) {
    case "CUSTOMER":
      return { name: "customer" };

    case "PROVIDER":
      return { name: "provider" };

    case "ADMIN":
      return { name: "admin" };

    default:
      return { name: "login" };
  }
}

async function handleSubmit(): Promise<void> {
  errorMessage.value = "";

  if (!email.value.trim()) {
    errorMessage.value = "Please enter your email address.";
    return;
  }

  if (!password.value) {
    errorMessage.value = "Please enter your password.";
    return;
  }

  isSubmitting.value = true;

  try {
    const response = await login({
      email: email.value.trim(),
      password: password.value,
    });

    authStore.setSession(
      response.user,
      response.access_token,
    );

    await router.replace(
      getDashboardRoute(response.user.role),
    );
  } catch (error) {
    if (error instanceof ApiError) {
      errorMessage.value = error.message;
    } else {
      errorMessage.value =
        "Something went wrong. Please try again.";
    }
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-brand">
      <RouterLink to="/" class="brand">
        <span class="brand-mark">S-</span>
        <span>ServiceHub</span>
      </RouterLink>
    </div>

    <main class="auth-content">
      <section class="auth-card">
        <div class="auth-header">
          <h1>Welcome back</h1>

          <p>
            Sign in to your ServiceHub account.
          </p>
        </div>

        <form
          class="auth-form"
          @submit.prevent="handleSubmit"
        >
          <div
            v-if="errorMessage"
            class="form-alert"
            role="alert"
          >
            {{ errorMessage }}
          </div>

          <div class="form-field">
            <label for="login-email">
              Email address
            </label>

            <input
              id="login-email"
              v-model="email"
              type="email"
              name="email"
              autocomplete="email"
              placeholder="you@example.com"
              :disabled="isSubmitting"
              required
            />
          </div>

          <div class="form-field">
            <div class="field-label-row">
              <label for="login-password">
                Password
              </label>

              <button
                type="button"
                class="password-toggle"
                :disabled="isSubmitting"
                @click="showPassword = !showPassword"
              >
                {{
                  showPassword
                    ? "Hide"
                    : "Show"
                }}
              </button>
            </div>

            <input
              id="login-password"
              v-model="password"
              :type="
                showPassword
                  ? 'text'
                  : 'password'
              "
              name="password"
              autocomplete="current-password"
              placeholder="Enter your password"
              :disabled="isSubmitting"
              required
            />
          </div>

          <button
            type="submit"
            class="submit-button"
            :disabled="!canSubmit"
          >
            <span v-if="isSubmitting">
              Signing in...
            </span>

            <span v-else>
              Sign in
            </span>
          </button>
        </form>

        <div class="auth-footer">
          <span>
            Don't have an account?
          </span>

          <RouterLink to="/register">
            Create an account
          </RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.auth-page {
  width: 100%;
}

.auth-card {
  width: 100%;
  padding: var(--space-10);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-surface);
  box-shadow: var(--shadow-lg);
}

.auth-header {
  margin-bottom: var(--space-8);
  text-align: center;
}

.auth-header h1 {
  margin: 0 0 var(--space-2);
  color: var(--color-text-primary);
  font-size: 1.8rem;
  line-height: 1.2;
}

.auth-header p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.form-alert {
  padding: var(--space-3) var(--space-4);
  border: 1px solid rgb(220 38 38 / 0.25);
  border-radius: var(--radius-md);
  background: rgb(220 38 38 / 0.08);
  color: var(--color-danger);
  font-size: 0.9rem;
  line-height: 1.5;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-field label {
  color: var(--color-text-primary);
  font-size: 0.9rem;
  font-weight: 600;
}

.field-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.password-toggle {
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--color-primary);
  font-size: 0.85rem;
  font-weight: 600;
}

.password-toggle:hover:not(:disabled) {
  color: var(--color-primary-hover);
}

.form-field input {
  width: 100%;
  min-height: 46px;
  padding: 0 var(--space-4);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  outline: none;
  background: var(--color-surface);
  color: var(--color-text-primary);
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast);
}

.form-field input::placeholder {
  color: var(--color-text-muted);
}

.form-field input:focus {
  border-color: var(--color-primary);
  box-shadow:
    0 0 0 3px
    color-mix(
      in srgb,
      var(--color-focus-ring) 35%,
      transparent
    );
}

.form-field input:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.submit-button {
  width: 100%;
  min-height: 46px;
  margin-top: var(--space-2);
  border: 0;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: var(--color-text-inverse);
  font-weight: 700;
  transition:
    background-color var(--transition-fast),
    opacity var(--transition-fast);
}

.submit-button:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.submit-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.auth-footer {
  display: flex;
  justify-content: center;
  gap: var(--space-2);
  margin-top: var(--space-8);
  color: var(--color-text-secondary);
  font-size: 0.9rem;
}

.auth-footer a {
  color: var(--color-primary);
  font-weight: 600;
}

.auth-footer a:hover {
  color: var(--color-primary-hover);
}

@media (max-width: 600px) {
  .auth-card {
    padding: var(--space-6);
    border-radius: var(--radius-lg);
  }
}
</style>

