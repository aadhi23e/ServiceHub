# ServiceHub V1.0.0 — Database Tables

## 1. Purpose

This document defines the database tables required for ServiceHub V1.0.0.

The tables are derived from the V1.0.0 domain architecture:

```text
Identity
    ↓
Provider Organization
    ↓
Services / Locations / Availability
    ↓
Booking
    ↓
Assignment / Travel / Execution
    ↓
Payment / Finance
    ↓
Reviews / Issues / Disputes
    ↓
Notifications / Audit / Administration
```

This document defines:

* table names
* responsibility of each table
* major relationships
* ownership of data
* why the table exists

It does **not** define the final SQLAlchemy models, columns, indexes, constraints, or migrations.

Those will be designed after the table structure is agreed.

---

# 2. Database Design Principles

## 2.1 PostgreSQL is the source of truth

PostgreSQL stores persistent business data.

Redis is not the source of truth for:

* users
* providers
* services
* bookings
* assignments
* payments
* financial records

Redis is supporting infrastructure for things such as:

* caching
* rate limiting
* temporary state
* background-job coordination

---

## 2.2 Tables represent domain responsibilities

A table should exist because the application has a meaningful business concept that needs to be persisted.

The goal is not to create a table for every possible object.

---

## 2.3 Historical information must be preserved

Bookings, assignments, payments, and administrative actions represent historical events.

Changing current provider or user information should not make historical records impossible to understand.

---

## 2.4 Provider-wide scheduling is not used

V1 does **not** use the old model:

```text
provider_id + start_at + end_at
```

as the primary booking conflict rule.

The scheduling resource is normally the individual agent:

```text
Booking
    ↓
Assignment
    ↓
Agent
```

This allows multiple agents belonging to the same provider to work simultaneously.

---

# 3. Table Overview

The V1.0.0 database is organized into the following groups.

```text
Identity & Provider
├── users
├── provider_organizations
└── provider_memberships

Provider Operations
├── provider_locations
├── provider_operating_hours
├── provider_service_areas
├── agent_availability
└── agent_time_off

Service Catalog
├── service_categories
├── services
└── service_requirements

Booking & Scheduling
├── bookings
├── booking_locations
├── booking_assignments
├── booking_status_history
└── booking_travel

Payments & Finance
├── payments
├── transactions
├── refunds
├── invoices
└── provider_settlements

Customer Experience
├── reviews
├── service_issues
└── disputes

Platform Operations
├── notifications
├── audit_logs
└── provider_verifications
```

Total initial V1.0.0 table count:

```text
27 tables
```

This count is a design baseline. During implementation, two tables may be combined if a concrete requirement shows that a separate persistence model is unnecessary.

---

# 4. Identity & Provider Tables

## 4.1 `users`

### Purpose

Stores platform user accounts.

A user represents a person who can authenticate with ServiceHub.

A user may participate in multiple contexts.

Example:

```text
User
├── Customer
└── Provider Owner
```

### Responsibilities

Stores identity/account information such as:

* authentication identity
* account status
* basic user profile information
* account lifecycle information

### Relationships

```text
users
  │
  ├── provider_memberships
  ├── bookings
  ├── reviews
  ├── notifications
  ├── service_issues
  └── audit_logs
```

### Important rule

A `users` row is not equivalent to a provider organization or provider agent.

---

# 4.2 `provider_organizations`

### Purpose

Represents a provider business, company, shop, or service organization.

Example:

```text
ABC Home Services
XYZ Mobile Repair
```

### Responsibilities

Stores provider-level business information and lifecycle state.

Examples:

* organization identity
* business information
* operational status
* verification-related state

### Relationships

```text
provider_organizations
        │
        ├── provider_memberships
        ├── provider_locations
        ├── provider_operating_hours
        ├── provider_service_areas
        ├── services
        ├── bookings
        ├── provider_verifications
        └── provider_settlements
```

### Important rule

A provider organization can have many agents.

It is not a worker account.

---

# 4.3 `provider_memberships`

### Purpose

Connects a platform user to a provider organization.

This table defines the person's provider-scoped role.

Possible roles:

```text
OWNER
MANAGER
AGENT
```

### Example

```text
User A
   ↓
Provider Membership
   ↓
ABC Services
   ↓
OWNER
```

Another:

```text
User B
   ↓
Provider Membership
   ↓
ABC Services
   ↓
AGENT
```

### Responsibilities

Defines:

* which provider organization the user belongs to
* their provider role
* membership status
* provider-scoped access

### Important rule

Provider membership is separate from the platform user identity.

This allows:

```text
User
 ├── Customer
 └── Provider Owner
```

---

# 5. Provider Operations Tables

## 5.1 `provider_locations`

### Purpose

Stores physical locations belonging to a provider organization.

Example:

```text
ABC Services
├── Chennai Central
├── Chennai North
└── Chennai South
```

### Responsibilities

Represents locations where:

* customers can visit
* services can be performed
* agents may operate
* provider operations may occur

### Relationships

```text
provider_organizations
        ↓
provider_locations
        ↓
bookings
```

---

# 5.2 `provider_operating_hours`

### Purpose

Stores the normal operating schedule of a provider or provider location.

Example:

```text
Monday     09:00 - 18:00
Tuesday    09:00 - 18:00
Wednesday  09:00 - 18:00
```

### Responsibilities

Defines when the business/location generally operates.

### Important distinction

Provider operating hours are not individual agent schedules.

```text
Provider Hours
      ≠
Agent Availability
```

---

# 5.3 `provider_service_areas`

### Purpose

Defines where a provider offers services, particularly home services.

Example:

```text
ABC Plumbing

600001
600002
600003
```

### Responsibilities

Used to determine whether a customer location is eligible for a home-service booking.

### Relationship

```text
provider_organizations
        ↓
provider_service_areas
        ↓
booking_locations
```

### V1 scope

The initial implementation can use postal/pincode-based areas.

More advanced geographic/GIS rules can be added later.

---

# 5.4 `agent_availability`

### Purpose

Stores an individual agent's normal working schedule.

Example:

```text
Agent A
Monday
09:00 - 17:00
```

### Responsibilities

Defines when an agent is normally available for assignments.

### Relationship

```text
provider_memberships
        ↓
agent_availability
```

Only provider memberships representing agents should have agent availability records.

---

# 5.5 `agent_time_off`

### Purpose

Stores periods during which an agent is unavailable despite their normal schedule.

Examples:

* sick leave
* vacation
* personal leave
* training
* temporary provider-approved absence

### Example

```text
Agent A
Normal:
09:00 - 18:00

Time Off:
14:00 - 18:00
```

### Relationship

```text
Agent
  ↓
agent_time_off
```

### Scheduling role

Availability is calculated from:

```text
Agent Schedule
     -
Time Off
     -
Existing Assignments
     -
Travel / Buffer
```

---

# 6. Service Catalog Tables

## 6.1 `service_categories`

### Purpose

Stores platform-level categories used to organize services.

Examples:

```text
Home Maintenance
Electronics
Cleaning
Automotive
```

### Responsibilities

Supports:

* service discovery
* browsing
* filtering
* platform-level organization

### Ownership

Categories are platform-managed.

Admins control them.

---

# 6.2 `services`

### Purpose

Represents a service offered by a provider organization.

Example:

```text
Provider:
ABC Mobile Care

Category:
Mobile Repair

Service:
iPhone Screen Replacement
```

### Responsibilities

Stores provider-specific service offerings.

A service can define concepts such as:

* service name
* description
* price
* duration
* supported service modes
* active state
* provider ownership

### Relationships

```text
service_categories
        ↓
services
        ↑
provider_organizations
```

A provider can offer many services.

A category can contain many services.

---

# 6.3 `service_requirements`

### Purpose

Defines additional information required from the customer for a specific service.

Example:

```text
Service:
AC Repair

Requirements:
- AC type
- Brand
- Problem description
```

Another service:

```text
Mobile Repair

Requirements:
- Device model
- Damage description
```

### Responsibilities

Allows different services to require different customer information.

### Relationship

```text
services
   ↓
service_requirements
```

This prevents the booking system from requiring one fixed set of fields for every service.

---

# 7. Booking & Scheduling Tables

## 7.1 `bookings`

### Purpose

The central business record representing a customer's request to receive a service.

A booking connects:

```text
Customer
Provider
Service
Service Mode
Appointment
Location
Payment
Assignment
```

### Responsibilities

Stores the booking's core lifecycle and business state.

### Relationships

```text
users
  ↓
bookings
  ↓
provider_organizations
  ↓
services
```

A booking may then connect to:

```text
booking_locations
booking_assignments
booking_travel
payments
invoices
reviews
service_issues
```

### Important rule

A booking is not itself an agent assignment.

---

# 7.2 `booking_locations`

### Purpose

Stores the location associated with a specific booking.

For:

```text
HOME_SERVICE
```

the location represents the customer's service address.

For:

```text
AT_PROVIDER
```

the location references the provider location where the service will occur.

### Why this is separate

A customer's current profile address can change.

The historical booking should still retain the location relevant to that appointment.

### Relationship

```text
bookings
    ↓
booking_locations
```

---

# 7.3 `booking_assignments`

### Purpose

Connects a booking to the agent responsible for executing the service.

Example:

```text
Booking #123
     ↓
Assignment
     ↓
Agent A
```

### Responsibilities

Stores:

* assigned agent
* assignment lifecycle
* assignment timing
* assignment history
* reassignment information

### Critical design principle

This table replaces the old provider-wide scheduling assumption.

Instead of:

```text
Provider cannot have overlapping bookings
```

V1 uses:

```text
Agent cannot have conflicting assignments
```

This allows:

```text
09:00
Provider ABC
├── Agent A → Booking 1
├── Agent B → Booking 2
└── Agent C → Booking 3
```

simultaneously.

---

# 7.4 `booking_status_history`

### Purpose

Stores the historical transitions of a booking.

Example:

```text
PENDING
   ↓
CONFIRMED
   ↓
ASSIGNMENT_REQUIRED
   ↓
COMPLETED
```

### Responsibilities

Provides an audit/history trail for booking lifecycle changes.

### Why it exists

The current booking status alone cannot answer:

> What happened to this booking?

The history table can.

---

# 7.5 `booking_travel`

### Purpose

Stores travel-related scheduling information for bookings where travel matters.

Primarily used for home services.

### Responsibilities

Can represent concepts such as:

* travel requirement
* configured travel/buffer duration
* previous/next service relationship
* travel scheduling information

### Example

```text
Agent A

09:00 - 10:00
Customer A

10:00 - 10:30
Travel

10:30 - 11:30
Customer B
```

### V1 scope

V1 does not require real-time route optimization.

The table supports the domain without forcing a mapping provider into the initial implementation.

---

# 8. Payment & Financial Tables

## 8.1 `payments`

### Purpose

Represents the payment lifecycle associated with a booking.

### Responsibilities

Stores payment-level information such as:

* payment status
* payment method
* booking association
* payment provider/reference information where applicable

### Supported V1 concepts

```text
ONLINE / DUMMY
OFFLINE / CASH
```

### Relationship

```text
booking
   ↓
payment
```

---

# 8.2 `transactions`

### Purpose

Stores financial transaction records.

A transaction represents a financial movement associated with ServiceHub.

Examples:

```text
Customer Payment
Refund
Platform Commission
Provider Amount
```

### Responsibilities

Provides financial traceability.

### Important distinction

A payment represents the payment lifecycle.

A transaction represents the financial movement.

They should not automatically be treated as the same concept.

---

# 8.3 `refunds`

### Purpose

Stores money returned to a customer.

Example:

```text
Payment
   ↓
Refund Requested
   ↓
Refunded
```

### Responsibilities

Tracks:

* refund reason
* refund amount
* refund state
* associated payment/transaction

Refunds are separate from normal payments because a payment can exist without a refund.

---

# 8.4 `invoices`

### Purpose

Represents financial documents associated with completed or billable bookings.

### Responsibilities

Stores the invoice record associated with a service transaction.

Conceptually:

```text
Booking
   ↓
Invoice
   ↓
Payment
```

The exact invoice-generation workflow will be finalized during financial implementation.

---

# 8.5 `provider_settlements`

### Purpose

Tracks money owed to or settled with provider organizations after accounting for platform fees, refunds, and other applicable financial adjustments.

Example:

```text
Customer Payment
      ↓
Platform Commission
      ↓
Provider Amount
      ↓
Provider Settlement
```

### Responsibilities

Supports provider-side financial reconciliation and platform reporting.

---

# 9. Customer Experience Tables

## 9.1 `reviews`

### Purpose

Stores customer reviews of completed service experiences.

### Relationship

```text
Customer
   ↓
Completed Booking
   ↓
Review
```

### Responsibilities

Supports:

* customer feedback
* service reputation
* provider/service reviews

### Important distinction

A review is not a service complaint.

A customer may leave a review while separately reporting an issue.

---

# 9.2 `service_issues`

### Purpose

Stores operational problems reported during or after a service.

Examples:

* incomplete service
* late arrival
* required tools unavailable
* additional materials required
* customer unavailable
* unsatisfactory service
* service could not be completed

### Relationship

```text
Booking
   ↓
Service Issue
```

### Responsibilities

Tracks the issue from creation through resolution.

---

# 9.3 `disputes`

### Purpose

Represents a formal escalation of a service issue requiring structured resolution.

Example:

```text
Service Issue
     ↓
Dispute
     ↓
Provider Review
     ↓
Admin Escalation
```

### Responsibilities

Supports formal dispute handling and resolution history.

A dispute may result in:

* refund
* revisit
* reassignment
* rescheduling
* other resolution

---

# 10. Platform Operations Tables

## 10.1 `notifications`

### Purpose

Stores notifications delivered to users.

Examples:

```text
Booking Confirmed
Agent Assigned
Agent En Route
Service Completed
Payment Successful
Booking Rescheduled
Issue Updated
Provider Approved
```

### Relationship

```text
User
 ↓
Notifications
```

### Important principle

Notifications communicate domain events.

They should not become the source of truth for the underlying business operation.

---

# 10.2 `audit_logs`

### Purpose

Stores important administrative, security-sensitive, and operational actions.

Examples:

```text
Admin approved provider
Admin suspended user
Manager reassigned booking
Agent completed service
Admin issued refund
Role changed
```

### Responsibilities

Provides accountability and investigation history.

### Important distinction

Audit logs are not the same as business state history.

For example:

```text
booking_status_history
```

answers:

> How did the booking status change?

While:

```text
audit_logs
```

answers:

> Who performed an important action and when?

---

# 10.3 `provider_verifications`

### Purpose

Stores the provider organization's verification/review history.

Example:

```text
Provider Registered
       ↓
Pending Review
       ↓
Admin Review
       ↓
Approved
```

### Responsibilities

Preserves:

* verification attempts
* reviewer/admin
* verification outcome
* relevant timestamps
* review information

### Important distinction

Provider verification is separate from user authentication.

A user can have a valid account while their provider organization is still pending verification.

---

# 11. Major Relationship Map

The main relationships are:

```text
users
 │
 ├───────────────┐
 │               │
 │               ▼
 │       provider_memberships
 │               │
 │               ▼
 │       provider_organizations
 │               │
 │       ┌───────┼───────────────┐
 │       │       │               │
 │       ▼       ▼               ▼
 │   locations services       service areas
 │               │
 │               ▼
 │      service_requirements
 │
 ▼
bookings
 │
 ├── booking_locations
 │
 ├── booking_assignments
 │         │
 │         ▼
 │      Agent
 │
 ├── booking_travel
 │
 ├── booking_status_history
 │
 ├── payments
 │      ├── transactions
 │      └── refunds
 │
 ├── invoices
 │
 ├── reviews
 │
 └── service_issues
          │
          ▼
       disputes
```

---

# 12. Agent Relationship

An agent is represented by a platform user with an agent membership in a provider organization.

Conceptually:

```text
users
  │
  ▼
provider_memberships
  │
  ├── role = AGENT
  │
  ├── agent_availability
  │
  ├── agent_time_off
  │
  └── booking_assignments
```

This avoids creating a completely separate authentication system for agents.

---

# 13. Provider Ownership Relationship

A provider organization can have multiple provider members.

```text
Provider Organization
│
├── Owner
├── Manager
├── Manager
├── Agent
├── Agent
└── Agent
```

The membership table controls the relationship.

This allows the organization to scale beyond one worker.

---

# 14. Booking Relationship

The central booking relationship is:

```text
Customer
   │
   ▼
Booking
   │
   ├── Provider
   ├── Service
   ├── Location
   ├── Assignment
   ├── Travel
   ├── Payment
   ├── Invoice
   ├── Review
   └── Issue
```

The booking therefore acts as the central business record connecting the customer service experience to provider operations.

---

# 15. Scheduling Relationship

Scheduling is based primarily around the agent.

```text
Provider
   │
   └── Agent
        │
        ├── Availability
        ├── Time Off
        └── Assignments
                 │
                 ├── Booking A
                 ├── Booking B
                 └── Booking C
```

Actual availability is derived from:

```text
Provider Operating Hours
            +
Service Requirements
            +
Agent Availability
            -
Agent Time Off
            -
Existing Assignments
            -
Travel / Buffer
```

The exact availability algorithm will be implemented later.

---

# 16. Payment Relationship

```text
Booking
   │
   ▼
Payment
   │
   ├── Transaction
   │
   └── Refund
```

Financial settlement:

```text
Transaction
     │
     ├── Platform Commission
     │
     └── Provider Amount
                │
                ▼
        Provider Settlement
```

---

# 17. Customer Issue Relationship

```text
Booking
   │
   ├── Review
   │
   └── Service Issue
           │
           ▼
        Dispute
```

These are deliberately separate because they answer different business questions.

| Concept       | Purpose                      |
| ------------- | ---------------------------- |
| Review        | Customer feedback            |
| Service Issue | Operational problem          |
| Dispute       | Formal escalation/resolution |

---

# 18. Administrative Relationship

Platform administration operates across the system.

```text
Admin
 │
 ├── Users
 ├── Providers
 ├── Provider Verification
 ├── Services / Categories
 ├── Bookings
 ├── Payments
 ├── Issues / Disputes
 ├── Audit Logs
 └── Platform Reports
```

Admin actions that require historical accountability should generate appropriate audit records.

---

# 19. Proposed V1.0.0 Table List

|  # | Table                      | Domain         | Main Responsibility                    |
| -: | -------------------------- | -------------- | -------------------------------------- |
|  1 | `users`                    | Identity       | Platform user accounts                 |
|  2 | `provider_organizations`   | Provider       | Provider businesses                    |
|  3 | `provider_memberships`     | Provider       | User-to-provider role                  |
|  4 | `provider_locations`       | Provider       | Provider physical locations            |
|  5 | `provider_operating_hours` | Provider       | Business operating hours               |
|  6 | `provider_service_areas`   | Provider       | Home-service coverage                  |
|  7 | `agent_availability`       | Provider       | Agent schedules                        |
|  8 | `agent_time_off`           | Provider       | Agent unavailable periods              |
|  9 | `service_categories`       | Catalog        | Platform service categories            |
| 10 | `services`                 | Catalog        | Provider services                      |
| 11 | `service_requirements`     | Catalog        | Service-specific customer requirements |
| 12 | `bookings`                 | Booking        | Customer service booking               |
| 13 | `booking_locations`        | Booking        | Service location                       |
| 14 | `booking_assignments`      | Booking        | Agent assignment                       |
| 15 | `booking_status_history`   | Booking        | Booking lifecycle history              |
| 16 | `booking_travel`           | Scheduling     | Travel/buffer information              |
| 17 | `payments`                 | Finance        | Payment lifecycle                      |
| 18 | `transactions`             | Finance        | Financial movements                    |
| 19 | `refunds`                  | Finance        | Returned payments                      |
| 20 | `invoices`                 | Finance        | Billing documents                      |
| 21 | `provider_settlements`     | Finance        | Provider financial settlement          |
| 22 | `reviews`                  | Customer       | Customer feedback                      |
| 23 | `service_issues`           | Customer       | Service problems                       |
| 24 | `disputes`                 | Customer/Admin | Formal issue resolution                |
| 25 | `notifications`            | Platform       | User notifications                     |
| 26 | `audit_logs`               | Platform/Admin | Important action history               |
| 27 | `provider_verifications`   | Platform/Admin | Provider verification history          |

---

# 20. Tables Intentionally Not Carried Forward From V0.0.1

The old V0.0.1 architecture contained concepts that do not map directly to V1.

## `provider_profiles`

Old concept:

```text
One Provider Profile
       ↓
One Worker / Provider
```

V1 replaces this with:

```text
provider_organizations
        +
provider_memberships
```

because one provider organization can have multiple workers.

---

## `availability`

Old concept:

```text
Provider Availability
```

V1 separates this into:

```text
provider_operating_hours
agent_availability
agent_time_off
```

because business hours and worker availability are different concepts.

---

## Old provider-wide booking overlap constraint

The old design attempted to prevent overlapping bookings at the provider level.

V1 does not use that model.

Instead:

```text
booking
   ↓
booking_assignment
   ↓
agent
```

is the relevant scheduling relationship.

---

# 21. Tables vs Redis / Celery

Not everything in the architecture becomes a PostgreSQL table.

## PostgreSQL

Persistent business state:

```text
Users
Providers
Services
Bookings
Assignments
Payments
Financial records
Issues
Reviews
Audit records
```

## Redis

Supporting infrastructure:

```text
Rate limiting
Caching
Temporary coordination
Short-lived state
```

## Celery

Background execution:

```text
Notifications
Scheduled jobs
Cleanup
Async processing
Future recurring tasks
```

Redis and Celery therefore do not replace the domain tables.

---

# 22. Database Design Dependency Order

The table implementation should follow logical dependencies.

A reasonable implementation order is:

```text
1. users
       ↓
2. provider_organizations
       ↓
3. provider_memberships
       ↓
4. provider_locations
5. provider_operating_hours
6. provider_service_areas
7. agent_availability
8. agent_time_off
       ↓
9. service_categories
10. services
11. service_requirements
       ↓
12. bookings
13. booking_locations
14. booking_assignments
15. booking_status_history
16. booking_travel
       ↓
17. payments
18. transactions
19. refunds
20. invoices
21. provider_settlements
       ↓
22. reviews
23. service_issues
24. disputes
       ↓
25. notifications
26. audit_logs
27. provider_verifications
```

The actual Alembic migration order may differ slightly based on foreign-key dependencies.

---

# 23. Next Database Design Phase

This document intentionally stops before defining individual columns.

The next phase should define the schema for each table:

```text
Table
  ↓
Columns
  ↓
Data Types
  ↓
Primary Keys
  ↓
Foreign Keys
  ↓
Unique Constraints
  ↓
Check Constraints
  ↓
Indexes
  ↓
Delete / Update Behavior
  ↓
Business Constraints
```

For example, `booking_assignments` will need to answer:

```text
Which booking?
Which agent?
When assigned?
When does the assignment begin?
When does it end?
Was it reassigned?
What is its execution state?
```

Those details belong to the **V1.0.0 database schema/model design**, not this table inventory document.

---

# 24. Final V1.0.0 Database Model

At the conceptual level, ServiceHub V1.0.0 is built around:

```text
USER
 │
 ├── CUSTOMER
 │      │
 │      └───────────────┐
 │                      │
 └── PROVIDER MEMBER    │
          │             │
          ▼             │
   PROVIDER ORG         │
      │                 │
      ├── Locations     │
      ├── Hours          │
      ├── Service Areas  │
      ├── Services      │
      └── Agents        │
             │          │
             ├── Availability
             ├── Time Off
             └── Assignments
                         │
                         ▼
                      BOOKING
                         │
              ┌──────────┼───────────┐
              │          │           │
           Location   Assignment   Travel
                         │
                         ▼
                       Agent
                         │
                         ▼
                     Execution
                         │
          ┌──────────────┼──────────────┐
          │              │              │
       Payment        Review          Issue
          │                             │
     Transaction                     Dispute
          │
       Refund
          │
       Invoice
          │
     Settlement

Platform Administration
          │
     ┌────┴─────┐
     │          │
 Verification  Audit
     │          │
     └────┬─────┘
          │
     Notifications
```

This is the **V1.0.0 database table baseline** from which the SQLAlchemy models and Alembic migration design should be created.
