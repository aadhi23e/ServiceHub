<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import { register } from "../../api/auth";
import { ApiError } from "../../api/client";
import type { UserRole } from "../../types/router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");
const confirmPassword = ref("");

const role = ref<UserRole>("CUSTOMER");

const isSubmitting = ref(false);
const errorMessage = ref("");
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

function getDashboardRoute(selectedRole: UserRole) {
  switch (selectedRole) {
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

  if (!firstName.value.trim()) {
    errorMessage.value =
      "Please enter your first name.";
    return;
  }

  if (!lastName.value.trim()) {
    errorMessage.value =
      "Please enter your last name.";
    return;
  }

  if (!email.value.trim()) {
    errorMessage.value =
      "Please enter your email address.";
    return;
  }

  if (password.value.length < 8) {
    errorMessage.value =
      "Password must be at least 8 characters.";
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value =
      "Passwords do not match.";
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
      role: role.value,
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
      name: "login",
    });
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
        <span class="brand-mark">S</span>
        <span>ServiceHub</span>
      </RouterLink>
    </div>

    <main class="auth-content">
      <section class="auth-card">
        <div class="auth-header">
          <h1>Create your account</h1>

          <p>
            Join ServiceHub and get started.
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

          <div class="name-grid">
            <div class="form-field">
              <label for="register-first-name">
                First name
              </label>

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
              <label for="register-last-name">
                Last name
              </label>

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
            <label for="register-email">
              Email address
            </label>

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
              <span class="optional">
                Optional
              </span>
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

          <fieldset class="role-field">
            <legend>Account type</legend>

            <div class="role-options">
              <label
                class="role-option"
                :class="{
                  selected:
                    role === 'CUSTOMER',
                }"
              >
                <input
                  v-model="role"
                  type="radio"
                  value="CUSTOMER"
                  :disabled="isSubmitting"
                />

                <span>
                  <strong>Customer</strong>
                  <small>
                    Find and book services
                  </small>
                </span>
              </label>

              <label
                class="role-option"
                :class="{
                  selected:
                    role === 'PROVIDER',
                }"
              >
                <input
                  v-model="role"
                  type="radio"
                  value="PROVIDER"
                  :disabled="isSubmitting"
                />

                <span>
                  <strong>Provider</strong>
                  <small>
                    Offer and manage services
                  </small>
                </span>
              </label>
            </div>
          </fieldset>

          <div class="form-field">
            <label for="register-password">
              Password
            </label>

            <div class="password-wrapper">
              <input
                id="register-password"
                v-model="password"
                :type="
                  showPassword
                    ? 'text'
                    : 'password'
                "
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
                @click="
                  showPassword =
                    !showPassword
                "
              >
                {{
                  showPassword
                    ? "Hide"
                    : "Show"
                }}
              </button>
            </div>
          </div>

          <div class="form-field">
            <label for="register-confirm-password">
              Confirm password
            </label>

            <div class="password-wrapper">
              <input
                id="register-confirm-password"
                v-model="confirmPassword"
                :type="
                  showConfirmPassword
                    ? 'text'
                    : 'password'
                "
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
                @click="
                  showConfirmPassword =
                    !showConfirmPassword
                "
              >
                {{
                  showConfirmPassword
                    ? "Hide"
                    : "Show"
                }}
              </button>
            </div>
          </div>

          <button
            type="submit"
            class="submit-button"
            :disabled="!canSubmit"
          >
            <span v-if="isSubmitting">
              Creating account...
            </span>

            <span v-else>
              Create account
            </span>
          </button>
        </form>

        <div class="auth-footer">
          <span>
            Already have an account?
          </span>

          <RouterLink to="/login">
            Sign in
          </RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(
      circle at top right,
      var(--color-primary-soft),
      transparent 35%
    ),
    var(--color-background);
}

.auth-brand {
  padding: var(--space-6);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  color: var(--color-text-primary);
  font-size: 1.15rem;
  font-weight: 700;
}

.brand-mark {
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: var(--color-text-inverse);
  font-weight: 800;
}

.auth-content {
  flex: 1;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-6);
}

.auth-card {
  width: min(100%, 520px);
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

.role-field {
  margin: 0;
  padding: 0;
  border: 0;
}

.role-field legend {
  margin-bottom: var(--space-3);
}

.role-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.role-option {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  cursor: pointer;
  transition:
    border-color var(--transition-fast),
    background-color var(--transition-fast);
}

.role-option:hover {
  background: var(--color-surface-hover);
}

.role-option.selected {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
}

.role-option input {
  margin-top: 3px;
  accent-color: var(--color-primary);
}

.role-option span {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.role-option strong {
  color: var(--color-text-primary);
  font-size: 0.9rem;
}

.role-option small {
  color: var(--color-text-secondary);
  font-size: 0.78rem;
  line-height: 1.4;
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
  .auth-brand {
    padding: var(--space-4);
  }

  .auth-content {
    padding: var(--space-6) var(--space-4);
    align-items: flex-start;
  }

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
