# ServiceHub

ServiceHub is a full-stack local service booking and management platform that connects customers with service providers and gives providers and administrators the tools to manage bookings, services, availability, users, and platform operations.

The project is designed as a realistic production-oriented application, covering the complete lifecycle of a modern web application from development and testing to deployment, monitoring, debugging, and continuous improvement.

---

## What is ServiceHub?

ServiceHub is built around a simple workflow:

```text
Customer
   ↓
Discover a Service
   ↓
Choose a Provider
   ↓
View Available Time
   ↓
Create Booking
   ↓
Provider Accepts
   ↓
Service Takes Place
   ↓
Booking Completed
   ↓
Customer Leaves Review
```

At the same time, providers can manage their services, availability, and bookings, while administrators can manage the overall platform.

---

## What is it for?

ServiceHub is intended to solve the common problem of finding and booking local services through a single platform.

Examples of services that could eventually be offered include:

* Home cleaning
* Plumbing
* Electrical services
* Beauty services
* Appliance repair
* Personal services
* Tutoring
* Photography
* Other appointment-based local services

The initial system focuses on the core booking and management workflow rather than trying to implement every possible marketplace feature.

---

# Features

## Customer

Customers can:

* Register and log in
* Manage their profile
* Browse service categories
* Browse service providers
* View provider profiles
* View provider services
* View service availability
* Find available booking times
* Create bookings
* View upcoming and previous bookings
* View booking details
* Cancel eligible bookings
* Receive in-app notifications
* Review completed services
* View provider reviews

---

## Provider

Providers can:

* Register and log in
* Create and manage their provider profile
* Create services
* Edit services
* Activate/deactivate services
* Configure recurring availability
* Edit availability
* View incoming bookings
* Accept bookings
* Reject bookings
* Start bookings
* Complete bookings
* View relevant customer information
* Receive notifications
* View reviews

---

## Admin

Administrators can:

* Log in to the administration area
* View platform statistics
* View users
* View user details
* Suspend users
* Activate users
* View providers
* View bookings
* Manage service categories
* View audit logs

---

# Booking System

Booking is one of the core business systems in ServiceHub.

A booking moves through defined states:

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

The system prevents invalid state transitions.

It also protects against two customers booking overlapping time for the same provider.

PostgreSQL is used as the source of truth for booking consistency, including database-level protection against overlapping active bookings.

Adjacent bookings are allowed:

```text
10:00 ───────── 11:00
11:00 ───────── 12:00
```

Overlapping bookings for the same provider are rejected.

---

# Technology Stack

## Frontend

* Vue 3
* TypeScript
* Vite
* Pinia
* Vue Router
* Tailwind CSS

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy 2.x
* Alembic
* Uvicorn

## Database

* PostgreSQL

## Caching / Background Processing

* Redis
* Celery

## Infrastructure

* Docker
* Docker Compose
* GitHub Actions

## Testing

### Backend

* pytest
* HTTPX

### Frontend

* Vitest
* Vue Test Utils

---

# Architecture

ServiceHub uses a modular monolith architecture.

The initial system intentionally avoids unnecessary microservices and distributed infrastructure.

```text
                    ┌─────────────────┐
                    │     Browser     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Vue 3 App    │
                    │ TypeScript/Vite │
                    └────────┬────────┘
                             │ HTTP
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │ Modular Backend │
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
       ┌───────────┐   ┌───────────┐   ┌───────────┐
       │PostgreSQL │   │   Redis   │   │  Celery   │
       │   Source  │   │  Broker / │   │ Background│
       │ of Truth  │   │ Rate Limit│   │   Jobs    │
       └───────────┘   └───────────┘   └───────────┘
```

The architecture is designed so that individual application components can scale independently when required without introducing unnecessary distributed-system complexity at the beginning.

---

# Topics Covered

ServiceHub is also a practical software engineering project covering a broad range of topics.

## Backend Development

* REST API development
* FastAPI
* Pydantic validation
* SQLAlchemy
* Service-layer architecture
* Dependency injection
* Error handling
* API design
* Pagination
* Filtering
* Business logic

## Database Engineering

* PostgreSQL
* Relational database design
* Primary keys
* Foreign keys
* Constraints
* Indexes
* Transactions
* Database migrations
* Alembic
* Data integrity
* Concurrency control
* PostgreSQL exclusion constraints

## Authentication & Security

* Password hashing
* Authentication
* Authorization
* Role-based access control
* JWT/session management
* Ownership checks
* IDOR prevention
* Rate limiting
* Secure API design
* Sensitive data protection
* Audit logging

## Frontend Development

* Vue 3
* TypeScript
* Component architecture
* State management
* Routing
* Forms
* API integration
* Loading states
* Error states
* Empty states
* Authentication flows
* Role-based UI

## Background Processing

* Redis
* Celery
* Asynchronous jobs
* Notifications
* Scheduled tasks
* Retry handling

## DevOps & Infrastructure

* Docker
* Docker Compose
* Environment configuration
* Production configuration
* Database deployment
* Redis deployment
* CI/CD
* GitHub Actions
* Health checks
* Backups

## Testing

* Unit testing
* Integration testing
* API testing
* Frontend testing
* Authentication testing
* Authorization testing
* Database testing
* Concurrency testing
* Edge-case testing

## Production Engineering

* Structured logging
* Request IDs
* Error tracking
* Health checks
* Observability
* Performance investigation
* Debugging production issues
* Security improvements
* Database migrations
* Release management
* Incident investigation

---

# Project Structure

The repository is organized around the frontend, backend, infrastructure, migrations, documentation, and project configuration.

```text
ServiceHub/
│
├── .github/
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
│
├── backend/
│
├── frontend/
│
├── migrations/
│
├── docker/
│
├── docs/
│
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
├── docker-compose.yml
└── .gitignore
```

Directories and modules will be introduced as the corresponding functionality is implemented.

---

# Local Development
Local Service Booking & Management Platform.

Stack
-----

Frontend:
- Vue
- TypeScript
- Vite

Backend:
- Python
- FastAPI
- SQLAlchemy
- Alembic

Infrastructure:
- PostgreSQL
- Redis
- Celery
- Docker Compose

Development
-----------

Start the local stack:

docker compose -f docker-compose.local.yml up -d --build

Frontend:
http://localhost:5173

Backend:
http://localhost:8000

API documentation:
http://localhost:8000/docs

Health:
http://localhost:8000/health/live

## Prerequisites

Install the following before starting local development:

* Git
* Docker
* Docker Compose
* Python
* Node.js
* npm

Verify the installations:

```bash
git --version
docker --version
docker compose version
python --version
node --version
npm --version
```

---

# Clone the Repository

```bash
git clone <repository-url>
cd ServiceHub
```

---

# Environment Configuration

Create the appropriate environment files for local development.

Example configuration categories include:

```text
DATABASE_URL
REDIS_URL
SECRET_KEY
JWT configuration
Application environment
CORS configuration
```

Never commit real credentials, API keys, passwords, or production secrets to Git.

A local environment file should remain untracked.

---

# Start Infrastructure

ServiceHub uses Docker Compose for local infrastructure.

Start the required services:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Follow logs for a specific service:

```bash
docker compose logs -f postgres
```

```bash
docker compose logs -f redis
```

---

# Database Migrations

Database schema changes are managed through Alembic.

Run migrations:

```bash
alembic upgrade head
```

Check migration status:

```bash
alembic current
```

Create a migration after a deliberate schema change:

```bash
alembic revision --autogenerate -m "describe the schema change"
```

Generated migrations must always be reviewed before being applied.

---

# Start the Backend

Create and activate a Python virtual environment when running the backend directly:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the development server:

```bash
uvicorn backend.app.main:app --reload
```

The exact command may evolve with the backend package structure.

---

# Start the Frontend

Install frontend dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will provide the browser-based ServiceHub interface.

---

# Start Background Workers

Celery is used for background tasks such as notifications and scheduled processing.

A worker can be started with:

```bash
celery -A <celery_application> worker --loglevel=info
```

The exact application path will be documented once the worker module is implemented.

---

# Local Deployment with Docker Compose

The target local environment is designed to run the application using Docker Compose.

Conceptually:

```text
Docker Compose
│
├── Frontend
├── Backend
├── PostgreSQL
├── Redis
└── Celery Worker
```

Start the complete environment:

```bash
docker compose up --build
```

Stop the environment:

```bash
docker compose down
```

Stop and remove the local database volume only when intentionally resetting local data:

```bash
docker compose down -v
```

---

# Health Checks

The backend will expose health endpoints for operational checks.

Typical endpoints include:

```text
/health
/health/ready
```

These endpoints are intended to distinguish between:

* application process health
* dependency/readiness health

The exact endpoint behavior will be documented with the implemented API.

---

# Testing

Run backend tests with:

```bash
pytest
```

Run frontend tests with:

```bash
npm test
```

Frontend linting/build commands will be available through the project's `package.json` scripts.

Before submitting a change, run the relevant tests and checks locally.

---

# Development Workflow

ServiceHub follows a structured Git workflow.

```text
Issue
  ↓
Feature/Fix Branch
  ↓
Implementation
  ↓
Tests
  ↓
Pull Request
  ↓
CI
  ↓
Review
  ↓
develop
  ↓
Release
  ↓
main
```

Branch names and commit messages follow the project's contribution guidelines.

See:

[`CONTRIBUTING.md`](CONTRIBUTING.md)

for the complete development workflow.

---

# CI/CD

GitHub Actions is used for automated project checks.

The CI pipeline is intended to validate:

* backend tests
* frontend tests
* linting
* type checking
* application builds
* database migrations where applicable
* Docker builds where applicable

The production deployment pipeline will be added as the deployment environment is established.

---

# Production Deployment

The application is designed to be deployable using containerized services.

A production deployment can eventually be structured around:

```text
                    Internet
                       │
                       ▼
                  Frontend/CDN
                       │
                       ▼
                 Reverse Proxy
                       │
                       ▼
              FastAPI Application
                  │          │
                  │          └──────────────┐
                  ▼                         ▼
             PostgreSQL                  Redis
                  │                         │
                  │                         ▼
                  │                    Celery Workers
                  │
                  ▼
               Backups
```

The exact production infrastructure will depend on the deployment environment.

Production deployment documentation will be maintained separately in `docs/` as the infrastructure is implemented.

---

# Data & Security

ServiceHub treats PostgreSQL as the source of truth for application data.

Important security principles include:

* passwords are never stored in plaintext
* authentication is required for protected operations
* authorization is enforced on the server
* users can only access resources they are authorized to access
* administrative operations require administrator privileges
* production secrets are stored outside source control
* audit-sensitive operations are logged
* rate limiting is applied where appropriate
* database constraints enforce important data integrity rules

---

# Documentation

Project documentation will be expanded as the application grows.

Planned documentation includes:

```text
docs/
├── architecture/
├── api/
├── database/
├── deployment/
├── operations/
└── security/
```

The README provides the project overview.

Detailed development and contribution rules are documented in:

[`CONTRIBUTING.md`](CONTRIBUTING.md)

Release history is maintained in:

[`CHANGELOG.md`](CHANGELOG.md)

---

# License

License information will be added before public release.
