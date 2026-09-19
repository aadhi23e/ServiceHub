# Contributing to ServiceHub

Thank you for contributing to ServiceHub.

ServiceHub is developed as a production-oriented application. Even when working as a solo developer, the project follows a professional Git, testing, review, and release workflow.

---

## 1. Development Philosophy

Every change should be:

* Small enough to understand and review.
* Focused on one problem.
* Tested appropriately.
* Secure by default.
* Observable through logs and errors where appropriate.
* Compatible with the existing architecture unless a deliberate architectural change is being made.
* Ready to deploy after the appropriate release process.

Do not implement features as placeholders with the intention of "finishing them later."

If a feature is started, implement its current scope completely before moving to another feature.

---

## 2. Branch Strategy

ServiceHub uses two permanent branches:

```text
main
develop
```

### `main`

`main` represents production.

Rules:

* Never push directly to `main`.
* Every merge must represent a production-ready state.
* Production releases are tagged using semantic versioning.
* Example:

```text
v1.0.0
v1.1.0
v1.1.1
```

### `develop`

`develop` is the integration branch for the next release.

Feature and fix branches are merged into `develop`.

---

## 3. Temporary Branches

Use the following branch types:

| Branch       | Purpose                                             |
| ------------ | --------------------------------------------------- |
| `feature/*`  | New functionality                                   |
| `fix/*`      | Non-production bug fixes                            |
| `hotfix/*`   | Critical production fixes                           |
| `refactor/*` | Code restructuring without intended behavior change |
| `perf/*`     | Performance improvements                            |
| `security/*` | Security-related changes                            |
| `test/*`     | Test-specific work                                  |
| `docs/*`     | Documentation                                       |
| `chore/*`    | Maintenance                                         |
| `ci/*`       | CI/CD changes                                       |

Branch naming format:

```text
<type>/<short-description>
```

Examples:

```text
feature/customer-registration
feature/provider-booking-management
fix/booking-double-submit
hotfix/login-production-error
security/login-rate-limit
refactor/auth-service
perf/provider-search
test/booking-concurrency
docs/api-authentication
chore/docker-production
ci/github-actions
```

Use:

* lowercase
* hyphen-separated names
* short descriptions
* no spaces
* no vague names such as `feature/new`, `changes`, or `test`

When an issue number exists, include it when practical:

```text
feature/31-customer-booking
fix/42-booking-double-submit
```

---

## 4. Standard Development Workflow

The normal workflow is:

```text
Issue
  ↓
Create branch from develop
  ↓
Implement change
  ↓
Write/update tests
  ↓
Run local checks
  ↓
Commit changes
  ↓
Push branch
  ↓
Open Pull Request
  ↓
CI
  ↓
Review
  ↓
Merge into develop
  ↓
Delete branch
```

Example:

```bash
git switch develop
git pull origin develop

git switch -c feature/customer-registration
```

After implementation:

```bash
git status
git diff
```

Run the relevant tests and checks before committing.

---

## 5. Conventional Commits

ServiceHub uses Conventional Commits.

Format:

```text
<type>(<scope>): <description>
```

Examples:

```text
feat(auth): add customer registration
feat(auth): implement JWT authentication
feat(booking): add booking creation service
fix(auth): reject duplicate email registration
fix(booking): prevent invalid cancellation
security(auth): add login rate limiting
test(booking): add concurrent booking test
refactor(auth): extract authentication service
perf(provider): optimize service lookup
docs(api): document booking endpoints
ci: run backend tests on pull requests
chore(docker): add PostgreSQL service
```

### Allowed commit types

```text
feat
fix
refactor
perf
security
test
docs
ci
chore
build
```

### Commit rules

A commit should:

* represent one coherent engineering change
* compile/build successfully where applicable
* not intentionally break tests
* avoid unrelated changes
* use a meaningful description

Avoid commits such as:

```text
update
changes
stuff
final
final-final
working
test
new code
fix everything
```

If multiple unrelated changes exist, separate them into multiple commits.

---

## 6. Pull Requests

All changes intended for `develop` or `main` should go through a Pull Request.

PR titles should follow Conventional Commit style.

Examples:

```text
feat(auth): add customer registration
fix(booking): prevent duplicate bookings
security(auth): add login rate limiting
refactor(provider): simplify availability service
```

Every PR should explain:

* what changed
* why it changed
* how it was tested
* whether the database changed
* whether deployment configuration changed
* whether security considerations exist

Use the repository Pull Request template.

---

## 7. Testing Requirements

Tests should be added or updated when behavior changes.

Backend changes should normally include appropriate:

* unit tests
* API/integration tests

Frontend changes should normally include appropriate:

* component tests
* interaction tests
* relevant integration tests

Security-sensitive behavior must receive explicit testing.

Examples:

* authentication
* authorization
* IDOR protection
* role checks
* booking ownership
* booking concurrency
* rate limiting
* sensitive data exposure

A feature is not considered complete merely because the code works manually.

---

## 8. Database Changes

ServiceHub uses PostgreSQL with Alembic migrations.

Database schema changes must include an Alembic migration.

Do not manually modify production database tables.

Before opening a PR containing a migration:

1. Run the migration locally.
2. Verify the resulting schema.
3. Test the application against the migrated database.
4. Verify downgrade behavior when practical.
5. Include the migration in the PR.

Database changes must be backward-aware when the application is deployed incrementally.

---

## 9. Security

Security is part of normal development rather than a final-stage activity.

Do not commit:

* passwords
* API keys
* tokens
* private credentials
* production secrets
* `.env` files containing secrets
* database credentials

Security-sensitive changes should use the `security/*` branch type when appropriate.

Examples:

```text
security/auth-password-hashing
security/login-rate-limit
security/booking-idor-protection
```

Potential vulnerabilities should be treated as engineering issues and addressed promptly.

---

## 10. Pull Request Checklist

Before opening a PR:

* [ ] The change has a clear purpose.
* [ ] The branch is based on the latest `develop`.
* [ ] Relevant tests were added or updated.
* [ ] Existing tests pass.
* [ ] Linting/type checks pass where applicable.
* [ ] No secrets are committed.
* [ ] Database migrations are included when required.
* [ ] Logging/error handling was considered.
* [ ] Authorization was considered.
* [ ] Documentation was updated when necessary.
* [ ] The PR description is complete.

---

## 11. Releases

ServiceHub follows Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

Examples:

```text
1.0.0
1.1.0
1.1.1
```

### Major

Breaking changes:

```text
2.0.0
```

### Minor

Backward-compatible functionality:

```text
1.1.0
```

### Patch

Backward-compatible fixes:

```text
1.1.1
```

---

## 12. Release Workflow

When the next release is ready:

```text
develop
   ↓
release/v1.0.0
   ↓
release validation
   ↓
main
   ↓
tag v1.0.0
   ↓
GitHub Release
```

Create the release branch:

```bash
git switch develop
git pull origin develop

git switch -c release/v1.0.0
```

During release preparation, feature development is frozen.

Only release-related work should be performed, such as:

* bug fixes
* documentation
* configuration corrections
* migration fixes
* release notes
* deployment fixes

After validation, merge the release into `main` and tag it.

Example:

```bash
git switch main
git merge --no-ff release/v1.0.0

git tag -a v1.0.0 -m "Release ServiceHub v1.0.0"
git push origin main
git push origin v1.0.0
```

The release branch should also be merged back into `develop` when necessary.

---

## 13. Production Hotfixes

Critical production bugs start from `main`.

Example:

```text
main
 ↓
hotfix/login-production-error
 ↓
main
 ↓
v1.0.1
```

Example:

```bash
git switch main
git pull origin main

git switch -c hotfix/login-production-error
```

After the fix is validated:

```text
hotfix → main
hotfix → develop
```

This prevents the production fix from being lost in future releases.

---

## 14. Real-World Feedback Loop

ServiceHub is intended to be developed and maintained like a real production application.

After a release:

```text
Production
    ↓
Real usage
    ↓
Errors
    ↓
Logs
    ↓
Performance observations
    ↓
User feedback
    ↓
Feature requests
    ↓
Security findings
    ↓
Engineering backlog
    ↓
Next release
```

Do not automatically define future releases in advance.

After `v1.0.0`, the next release should be based on actual:

* bugs
* user feedback
* operational problems
* performance data
* security findings
* feature requests
* developer observations

This allows ServiceHub to evolve based on real-world usage.

---

## 15. Code Quality

Prefer:

* clear names
* small functions
* explicit business rules
* typed interfaces
* predictable error handling
* testable services
* clear module boundaries
* secure defaults

Avoid:

* unnecessary abstractions
* premature microservices
* duplicated business logic
* hidden side effects
* giant functions
* generic catch-all error handling
* unexplained magic values
* unnecessary dependencies

The goal is production-quality engineering without unnecessary complexity.

---

## 16. Definition of Done

A change is considered complete when:

1. The requested behavior is implemented.
2. Business rules are enforced.
3. Authorization is correct.
4. Errors are handled appropriately.
5. Relevant tests exist.
6. Existing tests pass.
7. Database migrations exist when required.
8. Logging is appropriate.
9. Documentation is updated when necessary.
10. The PR is ready for review.

For production releases, deployment and health checks must also pass.
