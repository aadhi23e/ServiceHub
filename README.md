# ServiceHub

**ServiceHub** is a full-stack service booking and management platform that connects customers with verified service providers and their service agents.

The platform is designed around real-world service operations such as **home services, shop-based services, scheduled appointments, provider teams, agent assignment, availability, service areas, bookings, payments, notifications, and administrative oversight**.

ServiceHub is being developed as a realistic production-oriented application, with a focus on maintainability, security, observability, data integrity, and practical scalability.

---

## Features

### Customer

Customers can:

* Create an account and authenticate securely.
* Manage their profile and contact information.
* Browse service categories.
* Search and discover available services.
* View service and provider information.
* Check whether a service is available at their location.
* Select a service delivery method:

  * Home service
  * At-provider/shop service
* Provide the information required for the requested service.
* View available appointment slots.
* Create and manage bookings.
* Track booking status.
* Receive booking and service notifications.
* View payment and invoice information.
* Confirm service completion.
* Report service issues or disputes.
* Request cancellation or rescheduling where applicable.
* Submit reviews after eligible completed services.

### Service Providers

Providers can:

* Register as a service provider.
* Manage their business/service location.
* Create and manage services.
* Define service categories and pricing.
* Define supported service types.
* Configure service areas.
* Manage operating hours.
* Add and manage service agents.
* Assign agents to bookings.
* Manage agent schedules and availability.
* View and manage customer bookings.
* Handle cancellations and rescheduling.
* Reassign bookings when an agent becomes unavailable.
* Track active service operations.
* Manage service completion.
* Monitor payments and provider earnings.
* View invoices and transaction records.
* Manage provider-side notifications.

### Service Agents

Service agents can:

* Access their own account and dashboard.
* View assigned bookings.
* View their schedule and availability.
* Accept or acknowledge assigned work.
* Start travel for a home-service booking.
* Mark themselves as en route.
* Confirm arrival at the customer location.
* Start the service.
* Complete the service.
* Record relevant service notes.
* Report problems during a service.
* Report unavailable tools, materials, or additional requirements.
* View their completed work and service history.

### Administrators

Administrators provide platform-level oversight.

They can:

* Manage customers.
* Manage providers.
* Review and approve provider verification.
* Manage provider service operations.
* Manage provider agents where appropriate.
* Manage service categories.
* Review services and provider information.
* Monitor bookings.
* Monitor platform activity.
* Manage suspicious or abusive accounts.
* Suspend or reactivate users/providers.
* Review audit logs.
* Monitor payments and transactions.
* Monitor platform commissions.
* Review disputes and reported problems.
* Monitor application health and operational status.
* Review platform statistics and reports.
* Manage platform configuration where authorized.

---

## Core Service Workflow

ServiceHub separates the **customer, provider organization, and service agent** concepts.

A typical service flow is:

```text
Customer
   │
   ├── Login
   │
   ├── Browse/Search
   │
   ├── Select Category
   │
   ├── Select Provider / Service
   │
   ├── Select Service Mode
   │      ├── HOME_SERVICE
   │      └── AT_PROVIDER
   │
   ├── Provide Service Details
   │
   ├── Provide / Select Location
   │
   ├── Check Availability
   │
   ├── Select Appointment
   │
   ├── Create Booking
   │
   └── Payment
          │
          ▼
      Booking
          │
          ▼
   Provider Assignment
          │
          ▼
      Service Agent
          │
          ├── ASSIGNED
          ├── EN_ROUTE
          ├── ARRIVED
          ├── IN_PROGRESS
          └── COMPLETED
          │
          ▼
   Completion / Invoice
          │
          ▼
   Customer Confirmation / Issue
```

The exact booking, payment, cancellation, rescheduling, dispute, and reassignment rules are implemented as explicit domain workflows rather than relying on a generic status update.

---

## Provider Organization Model

A provider does not necessarily represent one individual worker.

A provider may represent:

* An individual professional.
* A shop.
* A company.
* A local service business.
* A team of service agents.

For example:

```text
Service Provider
│
├── Business / Shop
│
├── Services
│
├── Service Areas
│
├── Operating Hours
│
└── Service Agents
      ├── Agent A
      ├── Agent B
      ├── Agent C
      └── ...
```

This allows a business to have multiple agents working simultaneously.

For example, a repair shop could have:

```text
Shop
│
├── Agent A → Shop appointments
├── Agent B → Home services
├── Agent C → Shop appointments
└── Agent D → Home services
```

Agents can have individual schedules and availability while the provider maintains the overall business configuration.

---

## Service Modes

ServiceHub supports different ways a service can be delivered.

### Home Service

The service agent travels to the customer's location.

```text
Provider / Agent
       │
       ▼
Customer Location
```

The platform can use the customer's location and the provider's service area to determine whether the service can be offered.

### At Provider

The customer travels to the provider's location.

```text
Customer
    │
    ▼
Provider / Shop
```

The provider's operating hours and agent availability determine appointment availability.

---

## Booking and Assignment

Booking availability is not based only on a provider's general opening hours.

ServiceHub considers multiple constraints, including:

* Provider operating hours.
* Service duration.
* Agent availability.
* Existing bookings.
* Service mode.
* Service area.
* Customer location.
* Travel requirements for home services.
* Required preparation or service information.
* Agent assignment.
* Reassignment when an agent becomes unavailable.

The platform is designed so that the booking system can evolve from simple scheduling into a more realistic resource and workforce scheduling system.

---

## Booking Lifecycle

A booking can move through controlled domain states.

For example:

```text
PENDING
   │
   ├── CONFIRMED
   │      │
   │      ├── ASSIGNED
   │      │      │
   │      │      ├── EN_ROUTE
   │      │      │      │
   │      │      │      ├── ARRIVED
   │      │      │      │      │
   │      │      │      │      └── IN_PROGRESS
   │      │      │      │              │
   │      │      │      │              └── COMPLETED
   │      │      │      │
   │      │      │      └── ...
   │      │      │
   │      │      └── REASSIGNED
   │      │
   │      └── CANCELLED
   │
   └── REJECTED
```

Only valid state transitions are allowed.

The system will also support operational situations such as:

* Agent absence.
* Agent sickness.
* Late arrival.
* Customer unavailable.
* Service requiring additional equipment.
* Service requiring additional information.
* Customer dissatisfaction.
* Cancellation.
* Rescheduling.
* Agent reassignment.
* Service disputes.

---

## Payments

V1 includes a **dummy payment system** for development and testing.

The payment architecture is designed around a future real payment provider integration.

The system is intended to support:

* Payment records.
* Payment status.
* Transaction records.
* Invoices.
* Refund workflows.
* Provider earnings.
* Platform commission.
* Payment reconciliation.
* Online and offline payment workflows.

For offline payments, the provider-side workflow can record and reconcile payment collection rather than assuming that a successful booking automatically means successful payment.

---

## Provider Verification

Provider registration and provider verification are separate concepts.

A provider can register with the platform, but provider services intended for customers can require administrative verification.

```text
User
  │
  ▼
Provider Registration
  │
  ▼
Provider Profile
  │
  ▼
Verification
  │
  ▼
Admin Review
  │
  ├── Approved
  ├── Rejected
  └── Requires Changes
```

This provides a foundation for controlling which providers and services are allowed to operate on the platform.

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Alembic
* PostgreSQL
* Redis
* Celery
* Pydantic
* Argon2 password hashing
* JWT-based authentication

### Frontend

* TypeScript
* Vue
* Vite
* Pinia
* Vue Router
* Tailwind CSS
* Custom scoped CSS
* ESLint
* Prettier

### Infrastructure

* Docker
* Docker Compose
* GitHub Actions
* PostgreSQL
* Redis

### Development

* Git
* Conventional Commits
* Black
* Ruff
* ESLint
* Prettier
* Automated tests

---

## Architecture

ServiceHub uses a modular monolithic architecture.

```text
                         ┌─────────────────────┐
                         │      Vue Frontend    │
                         │ TypeScript + Pinia   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API      │
                         │ Authentication/RBAC  │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     │              │              │
                     ▼              ▼              ▼
                Services      Repositories      Domain
                     │              │              │
                     └──────────────┼──────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     PostgreSQL      │
                         └─────────────────────┘

                         ┌─────────────────────┐
                         │       Redis         │
                         │ Cache / Rate Limit  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       Celery        │
                         │ Background Jobs     │
                         └─────────────────────┘
```

The architecture intentionally avoids premature microservices and distributed infrastructure.

The goal is to keep V1 maintainable while maintaining clear boundaries that allow future extraction or scaling when required.

---

## Repository Structure

```text
ServiceHub/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── dependencies/
│   │   ├── enums/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements/
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── types/
│   │   └── views/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── docs/
├── .github/
├── docker-compose.local.yml
├── .env.example
├── Makefile
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

---

## Requirements

Before running ServiceHub locally, install:

* Git
* Docker Desktop
* Docker Compose
* Python 3.x for local backend development
* Node.js and npm for local frontend development

Docker is the recommended way to run the complete local development environment.

---

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Update the environment variables for your local environment.

Do not commit `.env` files or production secrets.

---

## Running Locally

Build and start the development stack:

```bash
docker compose -f docker-compose.local.yml up --build
```

Run in detached mode:

```bash
docker compose -f docker-compose.local.yml up -d --build
```

Stop the environment:

```bash
docker compose -f docker-compose.local.yml down
```

View logs:

```bash
docker compose -f docker-compose.local.yml logs -f
```

Run database migrations:

```bash
docker compose -f docker-compose.local.yml exec backend alembic upgrade head
```

The exact service names may vary with the current Docker Compose configuration.

---

## API Documentation

When the backend is running, FastAPI provides interactive API documentation.

Development documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative OpenAPI documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## API Versioning

ServiceHub APIs are versioned.

Current V1 API prefix:

```text
/api/v1
```

Example:

```text
GET /api/v1/users/me
```

API versioning allows future API changes without immediately breaking existing clients.

---

## Authentication and Authorization

ServiceHub uses authenticated accounts with role-based authorization.

Current platform roles include:

```text
CUSTOMER
PROVIDER
ADMIN
```

The application separates authentication from authorization.

Authentication determines:

> Who is the user?

Authorization determines:

> What is the user allowed to do?

Provider organizations and service agents are modeled separately so that a provider can operate as a business with multiple workers.

---

## Database

PostgreSQL is the primary relational database.

Database migrations are managed using Alembic.

Important application data includes:

* Users
* Provider profiles
* Service categories
* Services
* Provider agents
* Agent availability
* Provider operating hours
* Service areas
* Bookings
* Booking assignments
* Notifications
* Payments
* Transactions
* Invoices
* Reviews
* Audit logs

Database constraints and transactions are used to protect data integrity and prevent invalid application states.

---

## Testing

Backend tests can be run using the project's configured test command.

Example:

```bash
pytest
```

Frontend checks include:

```bash
npm run lint
npm run format:check
```

Where configured, CI runs automated validation before changes are merged.

---

## Code Quality

### Python

Python code follows:

* Black formatting
* Ruff linting
* Type hints
* PEP 8 conventions
* Clear module boundaries

Example:

```bash
black backend/
ruff check backend/
```

### TypeScript / Vue

Frontend code follows:

* ESLint
* Prettier
* TypeScript
* Vue conventions
* Explicit API types
* Reusable Pinia stores
* Component-level scoped styling where appropriate

Example:

```bash
npm run lint
npm run format
```

---

## Git Workflow

ServiceHub follows a feature-based Git workflow.

Typical development flow:

```text
feature branch
     │
     ▼
implementation
     │
     ▼
tests
     │
     ▼
pull request
     │
     ▼
review
     │
     ▼
merge
```

Branches should use descriptive names such as:

```text
feature/provider-agent-management
feature/booking-assignment
fix/service-availability
refactor/booking-domain
```

---

## Commit Convention

ServiceHub uses Conventional Commits.

Examples:

```text
feat: add provider agent management
feat: add booking assignment workflow
fix: prevent invalid booking transitions
refactor: separate provider and agent scheduling
test: add booking service tests
docs: update provider workflow
chore: update dependencies
```

---

## Versioning

ServiceHub follows Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

Current development milestone:

```text
V1.0.0
```

The previous architecture was developed as:

```text
V0.0.1
```

V1.0.0 represents a significant redesign around the real-world service marketplace workflow, including provider organizations, service agents, availability, service locations, booking assignment, verification, payments, and operational workflows.

Future releases may include:

```text
V1.x.x
```

for backward-compatible features and fixes, and:

```text
V2.0.0
```

for larger architectural or API-breaking changes.

---

## Development Principles

ServiceHub follows these principles:

1. **Build for real users.**
2. **Keep the architecture understandable.**
3. **Avoid premature enterprise complexity.**
4. **Protect data integrity at the database level.**
5. **Keep business rules inside appropriate service/domain boundaries.**
6. **Use explicit workflows instead of generic state mutations.**
7. **Design for multiple providers and multiple service agents.**
8. **Treat scheduling and availability as first-class domain concepts.**
9. **Keep payment and booking state separate.**
10. **Make operational failures recoverable.**
11. **Keep authentication and authorization separate.**
12. **Build V1 so it can evolve without requiring a complete rewrite.**

---

## Current Development Scope

V1.0.0 is being developed incrementally.

The major domain areas are:

```text
Authentication
      ↓
Users
      ↓
Providers
      ↓
Provider Organizations
      ↓
Service Agents
      ↓
Services
      ↓
Service Areas
      ↓
Availability
      ↓
Bookings
      ↓
Assignment
      ↓
Service Execution
      ↓
Payments
      ↓
Invoices
      ↓
Reviews / Disputes
      ↓
Notifications
      ↓
Administration / Audit
```

The implementation will be developed and tested domain-by-domain rather than introducing the entire system simultaneously.

---

## Contributing

Contributions should follow the project's coding standards and Git workflow.

Before submitting a pull request:

1. Create a feature or fix branch.
2. Make focused changes.
3. Add or update tests where appropriate.
4. Run formatting and linting.
5. Verify database migrations.
6. Verify the affected API workflows.
7. Update documentation when behavior changes.
8. Use a Conventional Commit message.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the project's detailed contribution guidelines.

---

## License

ServiceHub is currently under development.

The repository license should be defined before public distribution or production release.

If a license has been selected, it should be added as a `LICENSE` file in the repository root and referenced here.

---

## Project Status

**Current version:** `V1.0.0`

**Status:** Active development

ServiceHub V1.0.0 is focused on building a realistic service marketplace and operations platform rather than a simplified CRUD booking application.

The system is being developed incrementally with real-world scheduling, provider operations, service-agent assignment, payments, verification, notifications, and administrative workflows in mind.
