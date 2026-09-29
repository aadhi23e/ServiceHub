<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

import { register } from '../../api/auth';
import { ApiError } from '../../api/client';
import type { UserRole } from '../../types/router';

const router = useRouter();

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const phone = ref('');
const password = ref('');
const confirmPassword = ref('');

const role = ref<UserRole>('CUSTOMER');

const isSubmitting = ref(false);
const errorMessage = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const canSubmit = computed(() => {
  return (
    firstName.value.trim().length > 0 &&
    lastName.value.trim().length > 0 &&
    email.value.trim().length > 0 &&
    password.value.length >= 8 &&
    confirmPassword.value.length >= 8 &&
    password.value === confirmPassword.value &&
    !isSubmitting.value
  );
});

async function handleSubmit(): Promise<void> {
  errorMessage.value = '';

  if (!firstName.value.trim()) {
    errorMessage.value = 'Please enter your first name.';
    return;
  }

  if (!lastName.value.trim()) {
    errorMessage.value = 'Please enter your last name.';
    return;
  }

  if (!email.value.trim()) {
    errorMessage.value = 'Please enter your email address.';
    return;
  }

  if (password.value.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters.';
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match.';
    return;
  }

  isSubmitting.value = true;

  try {
    const user = await register({
      email: email.value.trim(),
      password: password.value,
      first_name: firstName.value.trim(),
      last_name: lastName.value.trim(),
      phone: phone.value.trim() || null,
    });

    /*
     * Registration creates the account.
     *
     * We do not assume registration returns
     * an access token. The user is redirected
     * to login after successful registration.
     */
    void user;

    await router.replace({
      name: 'login',
    });
  } catch (error) {
    if (error instanceof ApiError) {
      errorMessage.value = error.message;
    } else {
      errorMessage.value = 'Something went wrong. Please try again.';
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
          <h1>Create your account</h1>

          <p>Join ServiceHub and get started.</p>
        </div>

        <form class="auth-form" @submit.prevent="handleSubmit">
          <div v-if="errorMessage" class="form-alert" role="alert">
            {{ errorMessage }}
          </div>

          <div class="name-grid">
            <div class="form-field">
              <label for="register-first-name"> First name </label>

              <input
                id="register-first-name"
                v-model="firstName"
                type="text"
                name="first_name"
                autocomplete="given-name"
                placeholder="John"
                :disabled="isSubmitting"
                required
              />
            </div>

            <div class="form-field">
              <label for="register-last-name"> Last name </label>

              <input
                id="register-last-name"
                v-model="lastName"
                type="text"
                name="last_name"
                autocomplete="family-name"
                placeholder="Doe"
                :disabled="isSubmitting"
                required
              />
            </div>
          </div>

          <div class="form-field">
            <label for="register-email"> Email address </label>

            <input
              id="register-email"
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
            <label for="register-phone">
              Phone number
              <span class="optional"> Optional </span>
            </label>

            <input
              id="register-phone"
              v-model="phone"
              type="tel"
              name="phone"
              autocomplete="tel"
              placeholder="+91 98765 43210"
              :disabled="isSubmitting"
            />
          </div>

          <div class="form-field">
            <label for="register-password"> Password </label>

            <div class="password-wrapper">
              <input
                id="register-password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                name="password"
                autocomplete="new-password"
                placeholder="At least 8 characters"
                :disabled="isSubmitting"
                required
              />

              <button
                type="button"
                class="password-toggle"
                :disabled="isSubmitting"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>

          <div class="form-field">
            <label for="register-confirm-password"> Confirm password </label>

            <div class="password-wrapper">
              <input
                id="register-confirm-password"
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                name="confirm_password"
                autocomplete="new-password"
                placeholder="Re-enter your password"
                :disabled="isSubmitting"
                required
              />

              <button
                type="button"
                class="password-toggle"
                :disabled="isSubmitting"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                {{ showConfirmPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>

          <button type="submit" class="submit-button" :disabled="!canSubmit">
            <span v-if="isSubmitting"> Creating account... </span>

            <span v-else> Create account </span>
          </button>
        </form>

        <div class="auth-footer">
          <span> Already have an account? </span>

          <RouterLink to="/login"> Sign in </RouterLink>
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

.name-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-field label,
.role-field legend {
  color: var(--color-text-primary);
  font-size: 0.9rem;
  font-weight: 600;
}

.optional {
  margin-left: var(--space-1);
  color: var(--color-text-muted);
  font-size: 0.8rem;
  font-weight: 400;
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
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-focus-ring) 35%, transparent);
}

.form-field input:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.password-wrapper {
  position: relative;
}

.password-wrapper input {
  padding-right: 70px;
}

.password-toggle {
  position: absolute;
  top: 50%;
  right: var(--space-3);
  transform: translateY(-50%);
  padding: var(--space-1);
  border: 0;
  background: transparent;
  color: var(--color-primary);
  font-size: 0.85rem;
  font-weight: 600;
}

.password-toggle:hover:not(:disabled) {
  color: var(--color-primary-hover);
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

  .name-grid,
  .role-options {
    grid-template-columns: 1fr;
  }
}
</style>
