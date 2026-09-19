# ServiceHub Architecture Decision Records

This directory records important architectural and engineering decisions made for ServiceHub.

ADRs exist to document:

* what decision was made
* why it was made
* alternatives that were considered and rejected
* consequences of the decision
* when the decision should be reconsidered

An ADR documents a decision; it does not mean the decision can never change.

If a future requirement invalidates an existing decision, create a new ADR rather than silently changing the architecture.

---

## ADR Statuses

| Status       | Meaning                                                   |
| ------------ | --------------------------------------------------------- |
| `Proposed`   | Under discussion                                          |
| `Accepted`   | Decision has been made and should be followed             |
| `Superseded` | Replaced by a newer ADR                                   |
| `Deprecated` | No longer recommended but retained for historical context |
| `Rejected`   | Considered and explicitly rejected                        |

---

# Architecture Decisions

| ADR     | Decision                                                  | Status   |
| ------- | --------------------------------------------------------- | -------- |
| ADR-001 | Use a modular monolith architecture                       | Accepted |
| ADR-002 | Use Vue 3 + TypeScript for the frontend                   | Accepted |
| ADR-003 | Use FastAPI for the backend API                           | Accepted |
| ADR-004 | Use PostgreSQL as the primary database                    | Accepted |
| ADR-005 | Use SQLAlchemy 2.x as the ORM/database layer              | Accepted |
| ADR-006 | Use Alembic for database migrations                       | Accepted |
| ADR-007 | Use Redis for infrastructure, not as the source of truth  | Accepted |
| ADR-008 | Use Celery for background jobs                            | Accepted |
| ADR-009 | Use three application roles                               | Accepted |
| ADR-010 | Use application-level RBAC with resource ownership checks | Accepted |
| ADR-011 | Use explicit booking state transitions                    | Accepted |
| ADR-012 | Enforce booking overlap at the PostgreSQL level           | Accepted |
| ADR-013 | Store timestamps in UTC and retain provider timezone      | Accepted |
| ADR-014 | Use soft deactivation for important business entities     | Accepted |
| ADR-015 | Use REST APIs under `/api/v1`                             | Accepted |
| ADR-016 | Use centralized exception handling                        | Accepted |
| ADR-017 | Use structured logging and request IDs                    | Accepted |
| ADR-018 | Use layered observability                                 | Accepted |
| ADR-019 | Use Docker Compose for local infrastructure               | Accepted |
| ADR-020 | Use GitHub Actions for CI                                 | Accepted |
| ADR-021 | Use automated testing at multiple layers                  | Accepted |
| ADR-022 | Do not introduce file-upload/malware scanning in V1       | Accepted |
| ADR-023 | Use server-side authorization as the security authority   | Accepted |
| ADR-024 | Use database constraints for critical data integrity      | Accepted |
| ADR-025 | Keep V1 intentionally limited in scope                    | Accepted |
| ADR-026 | Use semantic versioning for releases                      | Accepted |
| ADR-027 | Use `main` and `develop` as permanent Git branches        | Accepted |
| ADR-028 | Use Conventional Commits                                  | Accepted |
| ADR-029 | Build future releases from real-world feedback            | Accepted |

---

# ADR-001 — Modular Monolith

**Status:** Accepted

## Decision

ServiceHub will initially be implemented as a **modular monolith**.

The backend will run as one FastAPI application while maintaining clear internal module boundaries.

```text
FastAPI
├── auth
├── users
├── providers
├── services
├── availability
├── bookings
├── reviews
├── notifications
└── admin
```

## Rationale

The application has a relatively small initial domain and does not require independent microservices to provide its core functionality.

A modular monolith provides:

* simple deployment
* simpler local development
* straightforward transactions
* easier debugging
* lower infrastructure complexity
* clear domain boundaries
* the ability to extract services later if a genuine need appears

## Alternatives Rejected

### Microservices

Rejected for V1 because they introduce:

* network boundaries
* service discovery
* distributed transactions
* more deployments
* more observability requirements
* more operational complexity

without a current requirement.

### Serverless-only architecture

Rejected because the application has persistent business workflows, background jobs, and database-heavy operations that are easier to reason about in a conventional application architecture.

## Consequences

Positive:

* faster development
* simpler deployment
* easier transactions
* easier debugging

Negative:

* the backend is initially deployed as one application
* module boundaries must be respected to avoid creating a monolithic code mess
* future service extraction may require additional work

---

# ADR-002 — Vue 3 + TypeScript Frontend

**Status:** Accepted

## Decision

The frontend will use:

* Vue 3
* TypeScript
* Vite
* Pinia
* Vue Router
* Tailwind CSS

## Rationale

This provides a modern typed frontend with a relatively small ecosystem and good support for component-based application development.

## Alternatives Rejected

### React

Rejected for this project because Vue provides a simpler component model for the intended application and matches the chosen development direction.

### Angular

Rejected because its larger framework structure is unnecessary for the initial application.

## Consequences

Positive:

* type safety
* component architecture
* predictable state management
* fast development experience

Negative:

* frontend developers need TypeScript knowledge
* additional build tooling is required

---

# ADR-003 — FastAPI Backend

**Status:** Accepted

## Decision

FastAPI will be the backend HTTP framework.

## Rationale

FastAPI provides:

* Python support
* type-driven request validation
* automatic OpenAPI documentation
* async support
* dependency injection
* good testing support

Python also aligns with the project's backend development goals.

## Alternatives Rejected

### Flask

Rejected for V1 because more API infrastructure would need to be assembled manually.

### Django

Rejected because the full Django framework is larger than necessary for the selected modular architecture.

## Consequences

Positive:

* strong typing
* automatic API documentation
* straightforward API development
* strong Python ecosystem

Negative:

* application architecture still needs to be designed carefully
* FastAPI does not automatically provide business-layer architecture

---

# ADR-004 — PostgreSQL as Source of Truth

**Status:** Accepted

## Decision

PostgreSQL will be the authoritative database for ServiceHub business data.

## Rationale

ServiceHub requires:

* relational integrity
* transactions
* foreign keys
* unique constraints
* indexing
* concurrent booking protection
* reliable persistence

PostgreSQL provides these capabilities directly.

## Alternatives Rejected

### MongoDB

Rejected because ServiceHub's core data is strongly relational.

### Redis as primary storage

Rejected because Redis is not the appropriate authoritative store for durable relational business data.

## Consequences

Positive:

* strong data integrity
* transactional booking operations
* mature database ecosystem

Negative:

* relational schema migrations must be managed carefully
* database scaling requires deliberate planning later

---

# ADR-005 — SQLAlchemy 2.x

**Status:** Accepted

## Decision

SQLAlchemy 2.x will be used as the application's database access and ORM layer.

## Rationale

SQLAlchemy provides:

* explicit database interaction
* transaction control
* PostgreSQL support
* mature ORM capabilities
* typed modern APIs

## Alternatives Rejected

### Raw SQL everywhere

Rejected because it would increase repetitive database mapping and maintenance work.

### Another Python ORM

Rejected because SQLAlchemy provides the required combination of ORM and low-level database control.

## Consequences

Developers must understand both:

* SQLAlchemy
* underlying PostgreSQL behavior

Important database constraints should not be hidden behind ORM abstractions.

---

# ADR-006 — Alembic Migrations

**Status:** Accepted

## Decision

All schema changes will be managed through Alembic migrations.

## Rationale

Production databases must be changed reproducibly.

Migrations provide:

* versioned schema changes
* deployment consistency
* rollback capability where practical
* team/CI reproducibility

## Alternatives Rejected

### Manual production SQL

Rejected because schema changes would become difficult to reproduce and audit.

### Recreate database from models

Rejected because production data must be preserved.

## Consequences

Every intentional schema change requires migration review and testing.

---

# ADR-007 — Redis Is Not the Source of Truth

**Status:** Accepted

## Decision

Redis will be used for:

* Celery broker functionality
* rate limiting
* selected caching

PostgreSQL remains authoritative.

## Rationale

Redis is excellent for fast temporary/stateful infrastructure operations but should not become the authoritative store for bookings or core business data.

## Alternatives Rejected

### Redis-based booking locks as the primary consistency mechanism

Rejected because database-level constraints provide a stronger final integrity boundary.

## Consequences

Some operations will involve both PostgreSQL and Redis, requiring careful failure handling.

---

# ADR-008 — Celery for Background Jobs

**Status:** Accepted

## Decision

Celery will process background tasks.

Initial tasks include:

* booking notifications
* reminders
* review notifications
* other non-critical asynchronous work

## Rationale

These operations should not unnecessarily block HTTP requests.

## Alternatives Rejected

### Execute everything inside HTTP requests

Rejected because slow/non-critical operations increase request latency and failure coupling.

### Kafka

Rejected because the V1 workload does not justify event-streaming infrastructure.

## Consequences

The system gains worker infrastructure and must handle:

* retries
* failures
* idempotency
* task monitoring

---

# ADR-009 — Three Application Roles

**Status:** Accepted

## Decision

V1 has exactly three roles:

```text
CUSTOMER
PROVIDER
ADMIN
```

## Rationale

These roles map directly to the product's primary actors.

## Alternatives Rejected

### Large permission hierarchy

Rejected for V1 because it adds complexity without a current requirement.

### Separate staff/moderator/operator roles

Deferred until a real operational requirement exists.

## Consequences

Future role expansion may require changes to authorization and UI behavior.

---

# ADR-010 — Application-Level RBAC + Ownership

**Status:** Accepted

## Decision

Authorization uses:

```text
Role/Permission
+
Resource Ownership
```

## Rationale

A role alone is insufficient.

For example, a provider may have permission to accept bookings but should only accept bookings belonging to that provider.

## Alternatives Rejected

### Frontend-only authorization

Rejected because clients cannot be trusted.

### Database-only authorization

Rejected because business authorization is more naturally expressed in application services for V1.

### Permission database

Rejected because the three-role system does not currently require dynamic permissions.

## Consequences

Authorization logic must be consistently implemented in the service layer.

---

# ADR-011 — Explicit Booking State Transitions

**Status:** Accepted

## Decision

Bookings use an explicit state machine.

```text
PENDING
 ├── CONFIRMED
 ├── REJECTED
 └── CANCELLED

CONFIRMED
 ├── CANCELLED
 └── IN_PROGRESS

IN_PROGRESS
 └── COMPLETED
```

## Rationale

Booking status represents business workflow, not an arbitrary editable property.

## Alternatives Rejected

### Generic status PATCH

Rejected because clients could attempt invalid transitions.

## Consequences

Each transition has explicit business logic and authorization.

---

# ADR-012 — Database-Level Booking Overlap Protection

**Status:** Accepted

## Decision

PostgreSQL will enforce the final booking overlap constraint using an exclusion constraint.

## Rationale

Application-level:

```text
check → insert
```

is vulnerable to concurrent requests.

The database must provide the final consistency boundary.

## Alternatives Rejected

### Redis lock

Rejected as the primary consistency mechanism.

### Application-only checking

Rejected because concurrent requests can bypass it.

### Serializable transactions everywhere

Rejected because the exclusion constraint directly expresses the required business invariant with less global complexity.

## Consequences

The application must translate PostgreSQL exclusion conflicts into:

```text
409 Conflict
```

---

# ADR-013 — UTC Storage + Provider Timezone

**Status:** Accepted

## Decision

Absolute timestamps are stored using PostgreSQL `TIMESTAMPTZ`.

Provider profiles contain an IANA timezone such as:

```text
Asia/Kolkata
```

Recurring availability is interpreted using the provider's timezone.

## Rationale

Scheduling is inherently timezone-sensitive.

## Alternatives Rejected

### Store all times as local time

Rejected because timezone ambiguity creates scheduling errors.

### Store everything as UTC without provider timezone

Rejected because recurring weekly availability requires knowing the provider's local calendar/time.

## Consequences

Timezone conversion must be handled carefully in the application and frontend.

---

# ADR-014 — Deactivation Instead of Destructive Deletion

**Status:** Accepted

## Decision

Important business entities are generally deactivated instead of physically deleted.

Examples:

```text
service.is_active = false
user.status = SUSPENDED
category.is_active = false
```

## Rationale

Historical bookings and audit records must remain meaningful.

## Alternatives Rejected

### Hard deletion

Rejected because it can break historical business relationships.

## Consequences

The database retains historical records and queries must distinguish active/inactive entities.

---

# ADR-015 — REST API + `/api/v1`

**Status:** Accepted

## Decision

The backend exposes REST-style APIs under:

```text
/api/v1/
```

## Rationale

The initial product is primarily CRUD and workflow oriented.

## Alternatives Rejected

### GraphQL

Rejected because it adds complexity that is not required by the initial UI.

### No API versioning

Rejected because introducing `/api/v1` from the beginning creates a clear future compatibility boundary.

## Consequences

Breaking API changes can be introduced under a future `/api/v2`.

---

# ADR-016 — Centralized Exception Handling

**Status:** Accepted

## Decision

Business exceptions are raised inside application services and translated into HTTP responses centrally.

## Rationale

Business logic should not depend directly on HTTP.

## Alternatives Rejected

### `HTTPException` throughout business code

Rejected because it couples domain logic to FastAPI.

## Consequences

The project needs:

* application exception classes
* centralized exception handlers
* consistent API error responses

---

# ADR-017 — Structured Logging + Request IDs

**Status:** Accepted

## Decision

Production logs will be structured and requests will receive correlation/request IDs.

## Rationale

Production debugging requires the ability to connect a user's failed request to the corresponding server logs.

## Alternatives Rejected

### Plain text logging only

Rejected because structured searching and automated analysis become harder.

### Logging every request body

Rejected because request bodies may contain sensitive information.

## Consequences

Logging must balance diagnostic value with privacy and security.

---

# ADR-018 — Layered Observability

**Status:** Accepted

## Decision

ServiceHub will initially use:

* structured logs
* request IDs
* health checks
* request timing
* application errors
* worker failure logging
* basic business/system metrics

More advanced observability can be added later.

## Alternatives Rejected

### Full observability stack from day one

Rejected because it adds operational complexity before there is enough production traffic to justify it.

## Consequences

Initial monitoring is intentionally lightweight and can evolve with actual production needs.

---

# ADR-019 — Docker Compose for Local Development

**Status:** Accepted

## Decision

Docker Compose will provide local infrastructure.

Initial services include:

```text
PostgreSQL
Redis
Backend
Celery Worker
Frontend
```

as appropriate to the development stage.

## Rationale

Compose provides reproducible local infrastructure without requiring Kubernetes.

## Alternatives Rejected

### Kubernetes locally

Rejected as unnecessary complexity.

### Install every dependency directly on the host

Rejected because environment differences become harder to control.

## Consequences

Developers need Docker installed and must understand container/network configuration.

---

# ADR-020 — GitHub Actions for CI

**Status:** Accepted

## Decision

GitHub Actions will run automated checks.

## Rationale

It integrates directly with the repository and Pull Request workflow.

## Alternatives Rejected

### No CI

Rejected because manual validation alone is insufficient for a production-oriented project.

### External CI platform

Deferred unless future requirements justify it.

## Consequences

CI configuration becomes part of the repository and must remain maintained.

---

# ADR-021 — Multi-Layer Automated Testing

**Status:** Accepted

## Decision

Testing will occur at multiple levels:

```text
Unit
Integration
API
Frontend
End-to-End
```

with the appropriate levels introduced as the application develops.

## Rationale

Different tests catch different classes of failures.

## Alternatives Rejected

### Only manual testing

Rejected because it does not reliably prevent regressions.

### Only end-to-end tests

Rejected because E2E tests are slower and less precise for many failures.

## Consequences

Tests become part of feature completion and increase development time, but reduce regression risk.

---

# ADR-022 — No File Upload/Malware Scanner in V1

**Status:** Accepted

## Decision

ServiceHub V1 will not include arbitrary file uploads.

Therefore V1 will not include an antivirus/malware scanning subsystem.

## Rationale

A security subsystem should solve an actual product requirement.

There is no V1 requirement for documents or arbitrary attachments.

## Alternatives Rejected

### Add ClamAV immediately

Rejected as unnecessary infrastructure for the current product.

## Consequences

If file uploads are introduced later, a new security architecture must be designed before enabling them.

That architecture should include:

```text
Upload
 ↓
Validation
 ↓
Size/type checks
 ↓
Malware scanning
 ↓
Quarantine
 ↓
Object storage
```

---

# ADR-023 — Server-Side Authorization Is Authoritative

**Status:** Accepted

## Decision

The backend is the authority for all security-sensitive authorization decisions.

## Rationale

Frontend state can be modified by an untrusted client.

## Alternatives Rejected

### Trust frontend role/user ID

Rejected because clients cannot be trusted.

## Consequences

Frontend authorization exists only for UX.

Every protected backend operation must independently verify authorization.

---

# ADR-024 — Database Constraints Protect Critical Invariants

**Status:** Accepted

## Decision

Critical data integrity rules should be enforced at the database level whenever practical.

Examples:

* foreign keys
* unique constraints
* check constraints
* booking overlap constraints

## Rationale

Business logic can contain bugs. The database provides a final integrity boundary.

## Alternatives Rejected

### Application validation only

Rejected because application validation can be bypassed by concurrency or future code paths.

## Consequences

Developers must understand database constraints and handle constraint violations correctly.

---

# ADR-025 — Intentionally Limited V1

**Status:** Accepted

## Decision

V1 focuses on the complete core booking workflow and the minimum production infrastructure required to operate it.

## Included

```text
Authentication
Profiles
Services
Categories
Availability
Bookings
Notifications
Reviews
Admin
Audit logs
Testing
Docker
CI
Logging
Health checks
```

## Excluded

```text
Payments
Chat
Maps
AI recommendations
Mobile application
Kubernetes
Kafka
Elasticsearch
Advanced analytics
Multi-country support
Multi-currency
Complex disputes
File uploads
```

## Rationale

A smaller complete production system provides more engineering value than a large incomplete system.

## Alternatives Rejected

### Build every planned feature before deployment

Rejected because it delays real-world validation.

## Consequences

Some useful functionality will intentionally remain outside V1.

---

# ADR-026 — Semantic Versioning

**Status:** Accepted

## Decision

Production releases use:

```text
MAJOR.MINOR.PATCH
```

## Rationale

Semantic versioning communicates release significance and compatibility expectations.

## Alternatives Rejected

### Date-only versions

Rejected because they do not directly communicate compatibility changes.

## Consequences

Release scope must be classified appropriately.

---

# ADR-027 — `main` + `develop`

**Status:** Accepted

## Decision

Two permanent branches are maintained:

```text
main
develop
```

Feature branches merge into `develop`.

Production releases merge into `main`.

## Rationale

The workflow provides a clear separation between integration and production.

## Alternatives Rejected

### Direct feature → main

Rejected because production should not be the primary integration environment.

### Large long-lived feature branches

Rejected because they increase merge conflicts and integration risk.

## Consequences

The project requires a release workflow and branch discipline.

---

# ADR-028 — Conventional Commits

**Status:** Accepted

## Decision

Git commits use Conventional Commit formatting.

Example:

```text
feat(booking): add booking creation
fix(auth): reject suspended users
security(booking): prevent unauthorized booking access
test(booking): add overlap concurrency test
```

## Rationale

Meaningful history makes the project easier to understand and maintain.

## Alternatives Rejected

### Free-form commit messages

Rejected because the history becomes harder to interpret.

## Consequences

Developers must maintain consistent commit naming.

---

# ADR-029 — Real-World Feedback Drives Future Releases

**Status:** Accepted

## Decision

After the first production release, future feature selection will be influenced by:

* real user feedback
* bugs
* logs
* performance data
* security findings
* operational problems
* feature requests
* developer observations

## Rationale

Future requirements cannot be known accurately before real users interact with the system.

## Alternatives Rejected

### Predefine every V2 feature now

Rejected because it would encourage building features without evidence of their importance.

## Consequences

The exact scope of later releases remains intentionally flexible.

The product backlog will evolve after production usage.
