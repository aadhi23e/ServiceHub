<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useUserStore } from '../../stores/users';

const userStore = useUserStore();

const firstName = ref('');
const lastName = ref('');
const phone = ref('');

const successMessage = ref('');
const localError = ref('');
const isEditing = ref(false);

const hasChanges = computed(() => {
  if (!userStore.user) {
    return false;
  }

  return (
    firstName.value !== userStore.user.first_name ||
    lastName.value !== userStore.user.last_name ||
    phone.value !== (userStore.user.phone ?? '')
  );
});

const initials = computed(() => {
  if (!userStore.user) {
    return '?';
  }

  const first = userStore.user.first_name?.trim().charAt(0) ?? '';
  const last = userStore.user.last_name?.trim().charAt(0) ?? '';

  return `${first}${last}`.toUpperCase() || '?';
});

const fullName = computed(() => {
  if (!userStore.user) {
    return 'Your Profile';
  }

  return `${userStore.user.first_name} ${userStore.user.last_name}`.trim();
});

const roleLabel = computed(() => {
  if (!userStore.user) {
    return '';
  }

  return formatRole(userStore.user.role);
});

const statusLabel = computed(() => {
  if (!userStore.user) {
    return '';
  }

  return formatStatus(userStore.user.status);
});

function formatRole(role: string): string {
  return role
    .toLowerCase()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function formatStatus(status: string): string {
  return status.toLowerCase().replace(/\b\w/g, (character) => character.toUpperCase());
}

function formatDate(value: string | null): string {
  if (!value) {
    return 'Not available';
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return 'Not available';
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date);
}

function populateForm(): void {
  if (!userStore.user) {
    return;
  }

  firstName.value = userStore.user.first_name;
  lastName.value = userStore.user.last_name;
  phone.value = userStore.user.phone ?? '';
}

function startEditing(): void {
  successMessage.value = '';
  localError.value = '';
  isEditing.value = true;
}

function cancelEditing(): void {
  populateForm();

  successMessage.value = '';
  localError.value = '';
  isEditing.value = false;
}

async function saveProfile(): Promise<void> {
  if (!userStore.user) {
    return;
  }

  successMessage.value = '';
  localError.value = '';

  const trimmedFirstName = firstName.value.trim();
  const trimmedLastName = lastName.value.trim();
  const trimmedPhone = phone.value.trim();

  if (!trimmedFirstName) {
    localError.value = 'First name is required.';
    return;
  }

  if (!trimmedLastName) {
    localError.value = 'Last name is required.';
    return;
  }

  try {
    await userStore.updateProfile({
      first_name: trimmedFirstName,
      last_name: trimmedLastName,
      phone: trimmedPhone || null,
    });

    populateForm();

    isEditing.value = false;
    successMessage.value = 'Your profile has been updated.';
  } catch {
    localError.value = userStore.error ?? 'Unable to update your profile.';
  }
}

async function loadProfile(): Promise<void> {
  localError.value = '';

  try {
    await userStore.fetchCurrentUser();
    populateForm();
  } catch {
    localError.value = userStore.error ?? 'Unable to load your profile.';
  }
}

onMounted(() => {
  loadProfile();
});
</script>

<template>
  <section class="profile-page">
    <!-- Page Header -->
    <header
      class="profile-page__header flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between"
    >
      <div class="profile-page__heading">
        <span class="profile-page__eyebrow"> Account </span>

        <h1>Profile</h1>

        <p>Manage your personal information and account details.</p>
      </div>

      <button
        v-if="!isEditing && userStore.user"
        type="button"
        class="profile-page__edit-button"
        @click="startEditing"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        >
          <path d="M12 20h9" />
          <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z" />
        </svg>

        <span>Edit profile</span>
      </button>
    </header>

    <!-- Loading -->
    <div v-if="userStore.loading && !userStore.user" class="profile-loading" aria-live="polite">
      <div class="profile-loading__spinner" />
      <p>Loading your profile...</p>
    </div>

    <!-- Error -->
    <div v-else-if="!userStore.user" class="profile-error" role="alert">
      <div class="profile-error__icon">!</div>

      <div>
        <h2>Unable to load profile</h2>
        <p>
          {{ localError || 'Something went wrong while loading your profile.' }}
        </p>

        <button type="button" class="profile-error__retry" @click="loadProfile">Try again</button>
      </div>
    </div>

    <!-- Profile -->
    <div v-else class="profile-layout">
      <!-- Main Profile Card -->
      <section class="profile-card profile-card--main">
        <!-- Profile identity -->
        <div class="profile-identity">
          <div class="profile-avatar" aria-hidden="true">
            {{ initials }}
          </div>

          <div class="profile-identity__content">
            <div class="profile-identity__name-row">
              <h2>{{ fullName }}</h2>

              <span
                class="profile-status"
                :class="`profile-status--${userStore.user.status.toLowerCase()}`"
              >
                <span class="profile-status__dot" />
                {{ statusLabel }}
              </span>
            </div>

            <p>{{ userStore.user.email }}</p>

            <span class="profile-role">
              {{ roleLabel }}
            </span>
          </div>
        </div>

        <div class="profile-card__divider" />

        <!-- Feedback -->
        <div v-if="successMessage" class="profile-alert profile-alert--success" role="status">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="m5 12 4 4L19 6" />
          </svg>

          <span>{{ successMessage }}</span>
        </div>

        <div v-if="localError" class="profile-alert profile-alert--error" role="alert">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="9" />
            <path d="M12 8v4" />
            <path d="M12 16h.01" />
          </svg>

          <span>{{ localError }}</span>
        </div>

        <!-- Personal information -->
        <div class="profile-section">
          <div class="profile-section__heading">
            <div>
              <h3>Personal information</h3>
              <p>Update the information associated with your ServiceHub account.</p>
            </div>
          </div>

          <form class="profile-form" @submit.prevent="saveProfile">
            <div class="profile-form__grid grid grid-cols-1 gap-5 md:grid-cols-2">
              <!-- First name -->
              <div class="profile-field">
                <label for="first-name"> First name </label>

                <input
                  id="first-name"
                  v-model="firstName"
                  type="text"
                  name="first_name"
                  autocomplete="given-name"
                  maxlength="100"
                  :disabled="!isEditing || userStore.saving"
                />
              </div>

              <!-- Last name -->
              <div class="profile-field">
                <label for="last-name"> Last name </label>

                <input
                  id="last-name"
                  v-model="lastName"
                  type="text"
                  name="last_name"
                  autocomplete="family-name"
                  maxlength="100"
                  :disabled="!isEditing || userStore.saving"
                />
              </div>

              <!-- Email -->
              <div class="profile-field">
                <label for="email"> Email address </label>

                <input
                  id="email"
                  :value="userStore.user.email"
                  type="email"
                  name="email"
                  autocomplete="email"
                  disabled
                />

                <span class="profile-field__hint">
                  Your email address cannot be changed here.
                </span>
              </div>

              <!-- Phone -->
              <div class="profile-field">
                <label for="phone"> Phone number </label>

                <input
                  id="phone"
                  v-model="phone"
                  type="tel"
                  name="phone"
                  autocomplete="tel"
                  maxlength="30"
                  :disabled="!isEditing || userStore.saving"
                  placeholder="Add a phone number"
                />
              </div>
            </div>

            <!-- Actions -->
            <div
              v-if="isEditing"
              class="profile-form__actions flex flex-col-reverse gap-3 sm:flex-row sm:justify-end"
            >
              <button
                type="button"
                class="profile-button profile-button--secondary"
                :disabled="userStore.saving"
                @click="cancelEditing"
              >
                Cancel
              </button>

              <button
                type="submit"
                class="profile-button profile-button--primary"
                :disabled="userStore.saving || !hasChanges"
              >
                <span v-if="userStore.saving" class="profile-button__spinner" />

                <span>
                  {{ userStore.saving ? 'Saving...' : 'Save changes' }}
                </span>
              </button>
            </div>
          </form>
        </div>
      </section>

      <!-- Account information -->
      <aside class="profile-card profile-card--account">
        <div class="profile-section__heading">
          <div>
            <h3>Account information</h3>
            <p>Details about your ServiceHub account.</p>
          </div>
        </div>

        <div class="account-details">
          <div class="account-detail">
            <span class="account-detail__label"> Account ID </span>

            <span class="account-detail__value"> #{{ userStore.user.id }} </span>
          </div>

          <div class="account-detail">
            <span class="account-detail__label"> Role </span>

            <span class="account-detail__value">
              {{ roleLabel }}
            </span>
          </div>

          <div class="account-detail">
            <span class="account-detail__label"> Account status </span>

            <span class="account-detail__value">
              {{ statusLabel }}
            </span>
          </div>

          <div class="account-detail">
            <span class="account-detail__label"> Member since </span>

            <span class="account-detail__value">
              {{ formatDate(userStore.user.created_at) }}
            </span>
          </div>

          <div class="account-detail">
            <span class="account-detail__label"> Last updated </span>

            <span class="account-detail__value">
              {{ formatDate(userStore.user.updated_at) }}
            </span>
          </div>

          <div class="account-detail">
            <span class="account-detail__label"> Last login </span>

            <span class="account-detail__value">
              {{ formatDate(userStore.user.last_login_at) }}
            </span>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.profile-page {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
}

/* ─────────────────────────────────────────────
   Header
───────────────────────────────────────────── */

.profile-page__header {
  margin-bottom: var(--space-6);
}

.profile-page__heading {
  min-width: 0;
}

.profile-page__eyebrow {
  display: block;
  margin-bottom: 4px;
  color: var(--color-text-muted);
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.profile-page__heading h1 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: clamp(1.5rem, 2vw, 1.85rem);
  font-weight: 750;
  letter-spacing: -0.025em;
  line-height: 1.2;
}

.profile-page__heading p {
  margin: 7px 0 0;
  max-width: 620px;
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
}

.profile-page__edit-button {
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-shrink: 0;
  padding: 0 15px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-primary);
  font-size: 0.82rem;
  font-weight: 700;
  box-shadow: var(--shadow-sm);
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    transform var(--transition-fast);
}

.profile-page__edit-button svg {
  width: 16px;
  height: 16px;
}

.profile-page__edit-button:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
}

.profile-page__edit-button:active {
  transform: translateY(1px);
}

.profile-page__edit-button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

/* ─────────────────────────────────────────────
   Layout
───────────────────────────────────────────── */

.profile-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 330px;
  gap: var(--space-5);
  align-items: start;
}

.profile-card {
  min-width: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}

.profile-card--main {
  overflow: hidden;
}

.profile-card--account {
  padding: var(--space-5);
}

/* ─────────────────────────────────────────────
   Identity
───────────────────────────────────────────── */

.profile-identity {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-6);
}

.profile-avatar {
  width: 72px;
  height: 72px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.profile-identity__content {
  min-width: 0;
}

.profile-identity__name-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 9px;
}

.profile-identity__name-row h2 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 1.2rem;
  font-weight: 750;
  line-height: 1.3;
}

.profile-identity__content > p {
  overflow: hidden;
  margin: 4px 0 8px;
  color: var(--color-text-secondary);
  font-size: 0.84rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-role {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 0 9px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  font-size: 0.67rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.profile-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 24px;
  padding: 0 8px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  font-size: 0.67rem;
  font-weight: 750;
}

.profile-status__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-text-muted);
}

.profile-status--active {
  color: var(--color-success);
}

.profile-status--active .profile-status__dot {
  background: var(--color-success);
}

.profile-status--suspended {
  color: var(--color-danger);
}

.profile-status--suspended .profile-status__dot {
  background: var(--color-danger);
}

.profile-card__divider {
  height: 1px;
  background: var(--color-border);
}

/* ─────────────────────────────────────────────
   Sections
───────────────────────────────────────────── */

.profile-section {
  padding: var(--space-6);
}

.profile-section__heading {
  margin-bottom: var(--space-5);
}

.profile-section__heading h3 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 0.98rem;
  font-weight: 750;
}

.profile-section__heading p {
  margin: 5px 0 0;
  color: var(--color-text-muted);
  font-size: 0.78rem;
  line-height: 1.5;
}

/* ─────────────────────────────────────────────
   Form
───────────────────────────────────────────── */

.profile-form__grid {
  width: 100%;
}

.profile-field {
  min-width: 0;
}

.profile-field label {
  display: block;
  margin-bottom: 7px;
  color: var(--color-text-secondary);
  font-size: 0.76rem;
  font-weight: 700;
}

.profile-field input {
  width: 100%;
  height: 42px;
  padding: 0 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  background: var(--color-surface);
  color: var(--color-text-primary);
  font-size: 0.84rem;
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    background-color var(--transition-fast);
}

.profile-field input:hover:not(:disabled) {
  border-color: var(--color-border-strong);
}

.profile-field input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.profile-field input:disabled {
  background: var(--color-surface-secondary);
  color: var(--color-text-secondary);
  cursor: not-allowed;
  opacity: 0.85;
}

.profile-field__hint {
  display: block;
  margin-top: 5px;
  color: var(--color-text-muted);
  font-size: 0.68rem;
  line-height: 1.4;
}

.profile-form__actions {
  margin-top: var(--space-6);
  padding-top: var(--space-5);
  border-top: 1px solid var(--color-border);
}

.profile-button {
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 16px;
  border-radius: var(--radius-md);
  font-size: 0.8rem;
  font-weight: 750;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast),
    box-shadow var(--transition-fast),
    transform var(--transition-fast);
}

.profile-button:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.profile-button:active:not(:disabled) {
  transform: translateY(1px);
}

.profile-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.profile-button--secondary {
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-secondary);
}

.profile-button--secondary:hover:not(:disabled) {
  background: var(--color-surface-hover);
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}

.profile-button--primary {
  border: 1px solid var(--color-primary);
  background: var(--color-primary);
  color: var(--color-text-inverse);
  box-shadow: var(--shadow-sm);
}

.profile-button--primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  box-shadow: var(--shadow-md);
}

.profile-button__spinner,
.profile-loading__spinner {
  width: 15px;
  height: 15px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: profile-spin 0.7s linear infinite;
}

@keyframes profile-spin {
  to {
    transform: rotate(360deg);
  }
}

/* ─────────────────────────────────────────────
   Alerts
───────────────────────────────────────────── */

.profile-alert {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin: 0 var(--space-6) var(--space-5);
  padding: 11px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 0.78rem;
  line-height: 1.45;
}

.profile-alert svg {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  margin-top: 1px;
}

.profile-alert--success {
  border-color: color-mix(in srgb, var(--color-success) 30%, var(--color-border));
  background: color-mix(in srgb, var(--color-success) 8%, var(--color-surface));
  color: var(--color-success);
}

.profile-alert--error {
  border-color: color-mix(in srgb, var(--color-danger) 30%, var(--color-border));
  background: color-mix(in srgb, var(--color-danger) 8%, var(--color-surface));
  color: var(--color-danger);
}

/* ─────────────────────────────────────────────
   Account information
───────────────────────────────────────────── */

.account-details {
  display: grid;
  gap: 0;
}

.account-detail {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  padding: 13px 0;
  border-top: 1px solid var(--color-border);
}

.account-detail:first-child {
  padding-top: 0;
  border-top: 0;
}

.account-detail:last-child {
  padding-bottom: 0;
}

.account-detail__label {
  color: var(--color-text-muted);
  font-size: 0.73rem;
}

.account-detail__value {
  max-width: 58%;
  color: var(--color-text-primary);
  font-size: 0.75rem;
  font-weight: 700;
  text-align: right;
}

/* ─────────────────────────────────────────────
   Loading / Error
───────────────────────────────────────────── */

.profile-loading {
  min-height: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
}

.profile-loading__spinner {
  width: 25px;
  height: 25px;
  border-width: 3px;
  color: var(--color-primary);
}

.profile-loading p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.profile-error {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: var(--space-6);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
}

.profile-error__icon {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-weight: 800;
}

.profile-error h2 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 0.95rem;
}

.profile-error p {
  margin: 5px 0 14px;
  color: var(--color-text-secondary);
  font-size: 0.78rem;
}

.profile-error__retry {
  min-height: 36px;
  padding: 0 13px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-primary);
  font-size: 0.76rem;
  font-weight: 700;
}

.profile-error__retry:hover {
  background: var(--color-surface-hover);
}

/* ─────────────────────────────────────────────
   Responsive
───────────────────────────────────────────── */

@media (max-width: 950px) {
  .profile-layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .profile-card--account {
    order: 2;
  }
}

@media (max-width: 640px) {
  .profile-page__header {
    margin-bottom: var(--space-4);
  }

  .profile-identity {
    align-items: flex-start;
    padding: var(--space-5);
  }

  .profile-avatar {
    width: 58px;
    height: 58px;
    border-radius: var(--radius-md);
    font-size: 1.05rem;
  }

  .profile-identity__name-row {
    align-items: flex-start;
    flex-direction: column;
    gap: 6px;
  }

  .profile-identity__name-row h2 {
    font-size: 1.05rem;
  }

  .profile-section {
    padding: var(--space-5);
  }

  .profile-alert {
    margin-right: var(--space-5);
    margin-left: var(--space-5);
  }

  .profile-card--account {
    padding: var(--space-5);
  }
}
</style>
