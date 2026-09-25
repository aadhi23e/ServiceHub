# ServiceHub V1.0.0 — Architecture

## 1. Purpose

This document defines the architecture of **ServiceHub V1.0.0**.

ServiceHub is a production-oriented local service booking and management platform connecting customers with service providers and their service agents.

The architecture is designed for:

* real users
* reliable booking and scheduling
* secure authentication and authorization
* horizontal backend scaling
* background job processing
* PostgreSQL as the source of truth
* Redis for supporting infrastructure
* independent frontend and backend deployment
* automated CI/CD
* observability and operational debugging
* incremental versioned releases

ServiceHub V1.0.0 is a **modular monolith application**.

The backend is intentionally not split into microservices.

---

# 2. Architecture Principles

ServiceHub follows these principles:

1. **Modular monolith first**
2. **Stateless backend**
3. **PostgreSQL as the source of truth**
4. **Redis as supporting infrastructure**
5. **Celery for asynchronous and scheduled work**
6. **Frontend and backend deploy independently**
7. **Horizontal backend scaling**
8. **Configuration through environment variables**
9. **Infrastructure differs between local development and production**
10. **CI validates changes before production deployment**
11. **Database migrations are version controlled**
12. **Production secrets never live in Git**
13. **Application components remain independently observable**
14. **Avoid distributed-system complexity unless the application actually requires it**

---

# 3. High-Level Architecture

```text
                         ┌──────────────────────┐
                         │       Users          │
                         │      Browser         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Frontend Delivery  │
                         │   Vue + Vite Build   │
                         │      CDN / Vercel    │
                         └──────────┬───────────┘
                                    │
                                    │ HTTPS / API
                                    ▼
                         ┌──────────────────────┐
                         │ Load Balancer /      │
                         │ Reverse Proxy        │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │ Backend #1 │  │ Backend #2 │  │ Backend #N │
             │  FastAPI   │  │  FastAPI   │  │  FastAPI   │
             └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
                   │               │               │
                   └───────────────┼───────────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
          ┌─────────────┐   ┌─────────────┐   ┌──────────────┐
          │ PostgreSQL  │   │    Redis    │   │    Celery    │
          │ Source of   │   │ Cache /     │   │   Workers    │
          │ Truth       │   │ Rate Limit /│   │              │
          │             │   │ Broker      │   │ Worker #1..N │
          └──────┬──────┘   └──────┬──────┘   └──────┬───────┘
                 │                 │                 │
                 ▼                 │                 │
             Backups              └─────────────────┘
```

---

# 4. Application Architecture

The backend follows a layered modular-monolith architecture.

```text
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
Dependencies
     │
     ├── Authentication
     ├── Authorization
     ├── Database Session
     ├── Redis
     └── Rate Limiting
     │
     ▼
Service Layer
     │
     ▼
Repository Layer
     │
     ▼
SQLAlchemy
     │
     ▼
PostgreSQL
```

The service layer contains business rules.

The repository layer handles persistence-oriented operations.

The API layer handles HTTP concerns.

This separation prevents business logic from becoming tightly coupled to HTTP endpoints.

---

# 5. Backend Architecture

ServiceHub uses a single FastAPI application containing multiple business modules.

Conceptually:

```text
FastAPI Application
│
├── Authentication
├── Users
├── Provider Organizations
├── Provider Members / Agents
├── Provider Locations
├── Services
├── Service Areas
├── Availability
├── Bookings
├── Booking Assignments
├── Scheduling
├── Payments
├── Invoices
├── Reviews
├── Issues / Disputes
├── Notifications
├── Administration
└── Health / Operations
```

These modules are part of one deployable backend application.

They are **not independent microservices**.

---

# 6. Stateless Backend

The FastAPI backend is designed to be stateless.

```text
                 Request
                    │
                    ▼
              Backend #1
                    │
                    ▼
               Response
```

The next request from the same user may reach another backend instance:

```text
                 Request
                    │
                    ▼
              Backend #3
                    │
                    ▼
               Response
```

The application must behave correctly in both cases.

User identity is established through authentication credentials, including the access token.

The backend does not depend on a particular server instance storing the user's application session in local memory.

This makes horizontal scaling possible.

---

# 7. Horizontal Backend Scaling

When traffic increases:

```text
Backend #1
Backend #2
Backend #3
...
Backend #N
```

can serve requests simultaneously.

A load balancer or hosting platform distributes requests between instances.

The backend instances share:

* PostgreSQL
* Redis
* application configuration
* authentication signing configuration
* required external services

They do not share local application state.

Therefore:

```text
Backend #1 ─┐
Backend #2 ─┤
Backend #3 ─┼──► PostgreSQL
Backend #N ─┤
            └──► Redis
```

The application should not rely on:

* local files for persistent application data
* in-memory user sessions
* in-memory distributed locks
* local-only queues
* instance-specific state

---

# 8. Frontend Architecture

The frontend is a Vue application built using Vite.

```text
Vue
│
├── Router
├── Pinia Stores
├── API Client
├── Views
├── Components
├── Types
└── Styling
```

The production frontend is a static/browser application.

It can therefore be deployed independently from the backend.

Example:

```text
servicehub.com
        │
        ▼
Frontend CDN
        │
        └──────────────► api.servicehub.com
                              │
                              ▼
                         FastAPI Backend
```

The frontend does not need to run inside the same production server as the backend.

---

# 9. PostgreSQL

PostgreSQL is the primary persistent data store.

It is the source of truth for application data.

It stores data such as:

* users
* provider organizations
* provider members
* agents
* services
* locations
* service areas
* schedules
* bookings
* booking assignments
* payments
* invoices
* reviews
* issues
* notifications
* audit records

PostgreSQL is responsible for durable relational data and database-level integrity.

Important integrity rules should be enforced through:

* foreign keys
* unique constraints
* check constraints
* indexes
* transactions
* appropriate concurrency controls

---

# 10. Redis

Redis is a supporting infrastructure component.

ServiceHub uses Redis for functionality such as:

* rate limiting
* Celery message brokering
* short-lived application data where appropriate
* distributed coordination where explicitly required

Redis is **not** the primary source of truth for business data.

Business-critical records must remain in PostgreSQL.

In production, Redis should preferably be provided as a managed/high-availability service rather than requiring the application team to operate a single Redis container manually.

---

# 11. Celery

Celery handles work that should not block an HTTP request.

Examples include:

```text
FastAPI
   │
   ├── create booking
   │
   ├── commit database transaction
   │
   └── enqueue background task
             │
             ▼
           Redis
             │
             ▼
       Celery Worker
             │
             ├── send notification
             ├── scheduled processing
             ├── reminder processing
             ├── cleanup tasks
             └── other asynchronous work
```

Celery workers are independently scalable.

For example:

```text
Celery Worker #1
Celery Worker #2
Celery Worker #3
```

can process jobs from the same queue.

The number of workers does not need to equal the number of backend instances.

---

# 12. Local Development Architecture

Local development uses Docker Compose.

The goal of the local environment is:

> Provide developers with a reproducible environment where the complete ServiceHub stack can be started with a small number of commands.

The local stack contains:

```text
docker-compose.local.yml

┌─────────────────────────────────────┐
│          Local Docker Host          │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ servicehub-frontend           │  │
│  └───────────────┬───────────────┘  │
│                  │                  │
│  ┌───────────────▼───────────────┐  │
│  │ servicehub-backend            │  │
│  └───────────────┬───────────────┘  │
│                  │                  │
│       ┌──────────┼───────────┐      │
│       ▼          ▼           ▼      │
│  servicehub-  servicehub- servicehub│
│  postgres     redis       celery    │
│                                     │
└─────────────────────────────────────┘
```

The `servicehub-` prefix is a **local container/service naming convention**.

It is not part of the production architecture.

---

# 13. Why Local and Production Are Different

Docker Compose exists primarily to make development predictable and convenient.

Production has different requirements:

```text
Local Development
-----------------
Docker Compose
Local PostgreSQL
Local Redis
Local Celery
Local Backend
Local Frontend
Developer-controlled configuration


Production
----------
CDN / Frontend hosting
Load balancing
Multiple backend instances
Managed PostgreSQL
Managed Redis
Multiple Celery workers
Production secrets
Monitoring
Backups
Deployment automation
```

The application code remains the same.

The infrastructure configuration changes.

This separation allows developers to reproduce the application locally without pretending that a single Docker Compose machine is equivalent to production infrastructure.

---

# 14. Local Service Networking

Inside Docker Compose, services communicate using their Docker service names.

Example:

```text
backend
   │
   ├──► postgres:5432
   │
   └──► redis:6379
```

The backend should not use:

```text
localhost:5432
localhost:6379
```

to reach PostgreSQL or Redis when those services are running in separate containers.

`localhost` refers to the current container.

The frontend/backend ports exposed to the host are different from internal Docker networking.

---

# 15. Production Networking

Production services communicate through their configured network endpoints.

Example:

```text
Frontend
   │
   │ HTTPS
   ▼
api.servicehub.com
   │
   ▼
Load Balancer
   │
   ├──► Backend #1
   ├──► Backend #2
   └──► Backend #N
```

The backend then connects to production infrastructure through environment configuration:

```text
DATABASE_URL
REDIS_URL
```

The actual hostname depends on the production infrastructure provider.

Application code should not hardcode production hostnames.

---

# 16. Environment Configuration

Configuration must be externalized.

Conceptually:

```text
Local
.env.local / Docker environment
        │
        ▼
Local PostgreSQL
Local Redis
Local services
```

while:

```text
Production
Secret / Environment Configuration
        │
        ▼
Production PostgreSQL
Production Redis
Production services
```

Examples of environment-dependent configuration include:

```text
DATABASE_URL
REDIS_URL
SECRET_KEY
JWT configuration
CORS origins
API base URL
application environment
logging configuration
```

Production secrets must never be committed to Git.

---

# 17. CI/CD Architecture

GitHub is the source repository.

GitHub Actions validates and releases the application.

The general pipeline is:

```text
Developer
    │
    ▼
Feature Branch
    │
    ▼
Pull Request
    │
    ▼
GitHub Actions
    │
    ├── Backend tests
    ├── Frontend tests
    ├── Linting
    ├── Type checking
    ├── Build validation
    └── Docker build validation
    │
    ▼
Code Review
    │
    ▼
Merge
    │
    ▼
Release / Deployment
    │
    ├── Frontend deployment
    └── Backend deployment
```

The exact deployment provider may evolve without changing the application architecture.

---

# 18. Versioned Releases

ServiceHub follows versioned releases.

Example:

```text
V0.0.1
   │
   ▼
V1.0.0
   │
   ├── V1.0.1
   ├── V1.0.2
   ├── V1.1.0
   └── V2.0.0
```

V0.0.1 represents the previous architecture.

V1.0.0 represents the redesigned production-oriented ServiceHub architecture.

A release should correspond to a known state of the application code and database migrations.

---

# 19. Container Images and Deployment

The backend should be packaged as a container image.

Conceptually:

```text
Git Repository
      │
      ▼
GitHub Actions
      │
      ▼
Build Backend Image
      │
      ▼
Container Registry
      │
      ▼
Production Backend
```

If multiple backend instances are required:

```text
Container Image
      │
      ├──► Backend #1
      ├──► Backend #2
      ├──► Backend #3
      └──► Backend #N
```

All instances run the same application version.

This is important for predictable deployments.

---

# 20. Database Migration Strategy

Database schema changes are managed through Alembic migrations.

Example:

```text
Developer changes model
        │
        ▼
Create Alembic migration
        │
        ▼
Test migration locally
        │
        ▼
CI migration validation
        │
        ▼
Production deployment
        │
        ▼
Run migration
        │
        ▼
Start/use new application version
```

Database migrations are version controlled together with the application.

Production migrations must be treated as deployment operations, not manual database edits.

---

# 21. Deployment Compatibility

Backend instances must be compatible with the database schema currently deployed.

For important schema changes, migrations should follow an additive/compatible approach where practical.

Example:

```text
Old Application
       │
       ▼
Compatible Database Migration
       │
       ▼
New Application
```

Avoid migrations that require the currently running application to immediately understand a completely incompatible schema.

This becomes increasingly important when multiple backend instances are running during deployment.

---

# 22. Stateless Authentication

The authentication design supports horizontally scaled backend instances.

Conceptually:

```text
                 Access Token
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Backend #1    Backend #2    Backend #N
        │             │             │
        └─────────────┼─────────────┘
                      │
                 User Identity
```

No individual backend instance owns a user's session.

Shared authentication configuration must be consistent across backend instances.

---

# 23. Background Job Scaling

Backend scaling and Celery scaling are independent.

For example:

```text
Traffic increases
       │
       ▼
Scale backend
       │
       ├──► Backend #1
       ├──► Backend #2
       └──► Backend #3
```

If background jobs increase:

```text
Job volume increases
       │
       ▼
Scale workers
       │
       ├──► Celery Worker #1
       ├──► Celery Worker #2
       ├──► Celery Worker #3
       └──► Celery Worker #N
```

This prevents HTTP request capacity and background-processing capacity from being unnecessarily coupled.

---

# 24. Observability

Each backend instance should produce structured logs suitable for centralized collection.

Important identifiers include:

```text
request_id
track_id
user_id where appropriate
operation
status
duration
error code
```

Health checks should distinguish between:

```text
Liveness
    │
    └── Is the application process running?

Readiness
    │
    └── Can the application access required dependencies?
```

The health system should not expose sensitive infrastructure information.

---

# 25. Failure Isolation

The architecture should prevent a failure in one supporting component from unnecessarily taking down the entire application.

Examples:

### Redis unavailable

Redis-dependent features should follow explicitly defined failure behavior.

For example, the existing rate-limiting design can fail open where appropriate rather than making the entire API unavailable.

### Celery unavailable

A background job system outage should be observable and recoverable.

Synchronous critical business transactions should not depend on a Celery worker completing before the HTTP request can succeed unless the business operation explicitly requires it.

### Backend instance unavailable

Traffic should be able to move to another healthy backend instance.

```text
Backend #1  ✕
Backend #2  ✓
Backend #3  ✓

             │
             ▼

        Application
        continues
```

---

# 26. Production Scaling Model

The expected scaling model for V1 is:

```text
                     ┌───────────────┐
                     │   Frontend    │
                     │   CDN / Host  │
                     └───────┬───────┘
                             │
                             ▼
                     ┌───────────────┐
                     │ Load Balancer │
                     └───────┬───────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
             Backend      Backend      Backend
                #1           #2           #N
                │            │            │
                └────────────┼────────────┘
                             │
               ┌─────────────┴─────────────┐
               │                           │
               ▼                           ▼
         PostgreSQL                     Redis
          Managed DB                  Managed Service
                                           │
                                           ▼
                                    Celery Workers
```

The backend is the primary horizontally scaled application component.

PostgreSQL and Redis are shared infrastructure services.

Celery workers scale according to background-job demand.

---

# 27. Why We Are Not Using Microservices

V1.0.0 contains multiple business domains, but that does not mean each domain needs its own service.

For example:

```text
Bookings
Payments
Providers
Notifications
Users
```

remain modules inside the same backend.

The application therefore avoids the operational cost of:

* service-to-service networking
* distributed tracing complexity
* multiple deployment pipelines
* independent service authentication
* duplicated configuration
* distributed transactions
* message contracts between many services

The modular structure still allows future extraction if a genuine scaling or ownership requirement appears.

---

# 28. Future Evolution

The architecture is intentionally designed so individual components can evolve.

Potential future evolution:

```text
V1.0.0

Modular Monolith
      │
      ▼
Scale Backend Horizontally
      │
      ▼
Improve Observability
      │
      ▼
Optimize Database
      │
      ▼
Scale Celery Workers
      │
      ▼
Introduce specialized infrastructure
only when justified
```

A future service extraction should be driven by an actual requirement such as:

* independent scaling
* independent deployment needs
* clear domain ownership
* operational isolation
* substantially different runtime requirements

It should not be introduced simply because the application has multiple domains.

---

# 29. Local-to-Production Relationship

The relationship between the two environments is:

```text
                  Same Application
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       Local Development      Production
              │                   │
              ▼                   ▼
       Docker Compose        Cloud Services
              │                   │
              ├── Frontend        ├── Frontend/CDN
              ├── Backend         ├── Backend #1..N
              ├── PostgreSQL      ├── Managed PostgreSQL
              ├── Redis           ├── Managed Redis
              └── Celery          └── Celery Workers
```

Docker Compose is therefore a **development environment**, not the definition of the entire production infrastructure.

The application code, migrations, tests, configuration contracts, and container images provide continuity between environments.

---

# 30. V1.0.0 Architectural Decision

For ServiceHub V1.0.0, the approved architecture is:

```text
Frontend
    │
    ▼
CDN / Frontend Hosting
    │
    ▼
Load Balancer / API Gateway
    │
    ▼
Stateless FastAPI Modular Monolith
    │
    ├──────────────► PostgreSQL
    │
    └──────────────► Redis
                         │
                         ▼
                   Celery Workers
```

### Local development

```text
Docker Compose

servicehub-frontend
servicehub-backend
servicehub-postgres
servicehub-redis
servicehub-celery
```

### Production

```text
Frontend/CDN
      +
Managed PostgreSQL
      +
Managed Redis
      +
Stateless FastAPI Backend #1..N
      +
Celery Worker #1..N
      +
Load Balancer
      +
CI/CD
      +
Monitoring / Logging / Backups
```

This architecture provides a realistic production foundation while keeping V1 operationally understandable and avoiding premature microservices or Kubernetes complexity.
