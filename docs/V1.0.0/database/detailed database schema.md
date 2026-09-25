# ServiceHub V1.0.0 — Detailed Database Schema

## 1. Global Database Conventions

### 1.1 Primary keys

All business tables use:

```text
UUID PRIMARY KEY
```

Recommended PostgreSQL implementation:

```python
id: Mapped[UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
)
```

Reason:

* safe for public APIs
* avoids predictable sequential IDs
* suitable for distributed application instances
* works well when the frontend/API exposes resource IDs

---

### 1.2 Timestamps

All timestamps use:

```text
TIMESTAMPTZ
```

Standard fields:

```text
created_at
updated_at
```

Where applicable, historical records also have:

```text
deleted_at
completed_at
cancelled_at
```

ServiceHub should store timestamps in UTC.

---

### 1.3 Money

Never use floating-point types for money.

Use:

```text
NUMERIC(12,2)
```

For larger financial aggregates:

```text
NUMERIC(14,2)
```

Every monetary record should also contain:

```text
currency CHAR(3)
```

V1 default:

```text
INR
```

---

### 1.4 Foreign-key deletion philosophy

Use:

```text
CASCADE
```

only where the child has no meaningful independent existence.

Use:

```text
RESTRICT
```

for financial, booking, audit, and historical records.

Use:

```text
SET NULL
```

when the historical record should remain after the referenced user/resource is removed.

Most real ServiceHub records should **not be physically deleted**.

Soft deletion/deactivation is preferred for:

* users
* providers
* services
* locations
* agents/memberships

---

# 2. Enum Definitions

The following enums are part of V1.0.0.

## User

```text
UserStatus
├── ACTIVE
├── SUSPENDED
└── DEACTIVATED
```

Provider organization:

```text
ProviderStatus
├── PENDING
├── ACTIVE
├── SUSPENDED
└── DEACTIVATED
```

Membership:

```text
ProviderMembershipRole
├── OWNER
├── MANAGER
└── AGENT
```

Membership status:

```text
MembershipStatus
├── INVITED
├── ACTIVE
├── SUSPENDED
└── REMOVED
```

Provider location:

```text
ProviderLocationType
├── SHOP
├── OFFICE
└── SERVICE_CENTER
```

Verification:

```text
VerificationStatus
├── PENDING
├── APPROVED
├── REJECTED
└── EXPIRED
```

Service:

```text
ServiceStatus
├── DRAFT
├── ACTIVE
├── INACTIVE
└── ARCHIVED
```

Service mode:

```text
ServiceMode
├── HOME_SERVICE
└── AT_PROVIDER
```

Requirement:

```text
RequirementType
├── TEXT
├── NUMBER
├── BOOLEAN
├── SINGLE_SELECT
├── MULTI_SELECT
└── FILE
```

Booking:

```text
BookingStatus
├── PENDING
├── CONFIRMED
├── ASSIGNMENT_PENDING
├── ASSIGNED
├── RESCHEDULED
├── IN_PROGRESS
├── COMPLETED
├── CANCELLED
├── NO_SHOW
└── DISPUTED
```

Assignment:

```text
AssignmentStatus
├── ASSIGNED
├── ACCEPTED
├── DECLINED
├── EN_ROUTE
├── IN_PROGRESS
├── COMPLETED
├── CANCELLED
└── REASSIGNED
```

Travel:

```text
TravelStatus
├── NOT_STARTED
├── EN_ROUTE
├── ARRIVED
├── CANCELLED
└── COMPLETED
```

Payment:

```text
PaymentStatus
├── PENDING
├── AUTHORIZED
├── PAID
├── FAILED
├── CANCELLED
├── REFUND_PENDING
└── REFUNDED
```

Payment method:

```text
PaymentMethod
├── DUMMY
├── CARD
├── UPI
├── NET_BANKING
└── WALLET
```

Transaction:

```text
TransactionType
├── PAYMENT
├── REFUND
├── COMMISSION
├── PROVIDER_SETTLEMENT
├── ADJUSTMENT
└── FEE
```

Refund:

```text
RefundStatus
├── PENDING
├── PROCESSING
├── COMPLETED
├── FAILED
└── CANCELLED
```

Invoice:

```text
InvoiceStatus
├── DRAFT
├── ISSUED
├── PAID
├── VOID
└── REFUNDED
```

Settlement:

```text
SettlementStatus
├── PENDING
├── PROCESSING
├── PAID
├── FAILED
└── CANCELLED
```

Review:

```text
ReviewStatus
├── PUBLISHED
├── HIDDEN
└── REMOVED
```

Issue:

```text
ServiceIssueStatus
├── OPEN
├── INVESTIGATING
├── RESOLVED
└── CLOSED
```

Dispute:

```text
DisputeStatus
├── OPEN
├── UNDER_REVIEW
├── RESOLVED
├── REJECTED
└── CLOSED
```

Notification:

```text
NotificationType
├── BOOKING_CREATED
├── BOOKING_CONFIRMED
├── BOOKING_ASSIGNED
├── BOOKING_RESCHEDULED
├── BOOKING_CANCELLED
├── PAYMENT_SUCCESS
├── PAYMENT_FAILED
├── SERVICE_STARTED
├── SERVICE_COMPLETED
├── REVIEW_REQUEST
└── SYSTEM
```

Notification status:

```text
NotificationStatus
├── UNREAD
├── READ
└── ARCHIVED
```

---

# 3. Identity & Provider Tables

# 3.1 `users`

Represents a platform user.

| Column           | Type         | Null | Key / Constraint |
| ---------------- | ------------ | ---: | ---------------- |
| `id`             | UUID         |   No | PK               |
| `email`          | VARCHAR(255) |   No | Unique           |
| `phone`          | VARCHAR(20)  |  Yes | Indexed          |
| `password_hash`  | VARCHAR(255) |   No |                  |
| `first_name`     | VARCHAR(100) |   No |                  |
| `last_name`      | VARCHAR(100) |  Yes |                  |
| `status`         | UserStatus   |   No | Default ACTIVE   |
| `is_admin`       | BOOLEAN      |   No | Default false    |
| `last_login_at`  | TIMESTAMPTZ  |  Yes |                  |
| `created_at`     | TIMESTAMPTZ  |   No |                  |
| `updated_at`     | TIMESTAMPTZ  |   No |                  |
| `deactivated_at` | TIMESTAMPTZ  |  Yes |                  |

### Constraints

```text
PK(id)
UNIQUE(lower(email))
```

Recommended:

```text
CHECK(length(first_name) > 0)
```

### Indexes

```text
idx_users_email
idx_users_phone
idx_users_status
```

### Delete behavior

Users should not normally be deleted.

Use:

```text
status = DEACTIVATED
```

Other tables referencing users should generally use:

```text
ON DELETE RESTRICT
```

or `SET NULL` for actor/history relationships.

---

# 3.2 `provider_organizations`

Represents a provider business.

| Column           | Type           | Null | Key / Constraint |
| ---------------- | -------------- | ---: | ---------------- |
| `id`             | UUID           |   No | PK               |
| `name`           | VARCHAR(200)   |   No |                  |
| `description`    | TEXT           |  Yes |                  |
| `status`         | ProviderStatus |   No | Default PENDING  |
| `email`          | VARCHAR(255)   |  Yes |                  |
| `phone`          | VARCHAR(20)    |  Yes |                  |
| `website`        | VARCHAR(500)   |  Yes |                  |
| `created_by`     | UUID           |   No | FK users         |
| `created_at`     | TIMESTAMPTZ    |   No |                  |
| `updated_at`     | TIMESTAMPTZ    |   No |                  |
| `deactivated_at` | TIMESTAMPTZ    |  Yes |                  |

### Foreign key

```text
created_by → users.id
ON DELETE RESTRICT
```

### Indexes

```text
idx_provider_org_status
idx_provider_org_created_by
```

### Business constraints

A provider cannot accept bookings unless:

```text
status = ACTIVE
```

---

# 3.3 `provider_memberships`

Connects users to provider organizations.

This replaces the old `provider_profiles` role model.

| Column        | Type                   | Null | Key / Constraint          |
| ------------- | ---------------------- | ---: | ------------------------- |
| `id`          | UUID                   |   No | PK                        |
| `provider_id` | UUID                   |   No | FK provider_organizations |
| `user_id`     | UUID                   |   No | FK users                  |
| `role`        | ProviderMembershipRole |   No |                           |
| `status`      | MembershipStatus       |   No |                           |
| `joined_at`   | TIMESTAMPTZ            |  Yes |                           |
| `removed_at`  | TIMESTAMPTZ            |  Yes |                           |
| `created_at`  | TIMESTAMPTZ            |   No |                           |
| `updated_at`  | TIMESTAMPTZ            |   No |                           |

### Unique

```text
UNIQUE(provider_id, user_id)
```

### Foreign keys

```text
provider_id → provider_organizations.id
ON DELETE RESTRICT

user_id → users.id
ON DELETE RESTRICT
```

### Indexes

```text
idx_membership_provider
idx_membership_user
idx_membership_provider_role
```

### Business constraints

Each provider should have exactly one active OWNER in normal operation.

A user can have:

```text
CUSTOMER behavior
+
provider OWNER membership
```

at the same time.

Provider role is therefore **organization-scoped**, not a global user role.

---

# 4. Provider Operations

# 4.1 `provider_locations`

Physical locations belonging to a provider.

| Column          | Type                 | Null | Key / Constraint |
| --------------- | -------------------- | ---: | ---------------- |
| `id`            | UUID                 |   No | PK               |
| `provider_id`   | UUID                 |   No | FK               |
| `name`          | VARCHAR(150)         |   No |                  |
| `location_type` | ProviderLocationType |   No |                  |
| `address_line1` | VARCHAR(255)         |   No |                  |
| `address_line2` | VARCHAR(255)         |  Yes |                  |
| `city`          | VARCHAR(100)         |   No |                  |
| `state`         | VARCHAR(100)         |   No |                  |
| `postal_code`   | VARCHAR(20)          |   No |                  |
| `country_code`  | CHAR(2)              |   No |                  |
| `latitude`      | NUMERIC(9,6)         |  Yes |                  |
| `longitude`     | NUMERIC(9,6)         |  Yes |                  |
| `is_active`     | BOOLEAN              |   No |                  |
| `created_at`    | TIMESTAMPTZ          |   No |                  |
| `updated_at`    | TIMESTAMPTZ          |   No |                  |

### FK

```text
provider_id → provider_organizations.id
ON DELETE RESTRICT
```

### Indexes

```text
idx_provider_locations_provider
idx_provider_locations_active
```

### Business constraints

```text
latitude BETWEEN -90 AND 90
longitude BETWEEN -180 AND 180
```

A location cannot be removed if historical bookings reference it.

---

# 4.2 `provider_operating_hours`

Provider/location business hours.

| Column        | Type        | Null | Key |
| ------------- | ----------- | ---: | --- |
| `id`          | UUID        |   No | PK  |
| `provider_id` | UUID        |   No | FK  |
| `location_id` | UUID        |  Yes | FK  |
| `day_of_week` | SMALLINT    |   No |     |
| `opens_at`    | TIME        |   No |     |
| `closes_at`   | TIME        |   No |     |
| `is_closed`   | BOOLEAN     |   No |     |
| `created_at`  | TIMESTAMPTZ |   No |     |
| `updated_at`  | TIMESTAMPTZ |   No |     |

### Foreign keys

```text
provider_id → provider_organizations.id
ON DELETE CASCADE

location_id → provider_locations.id
ON DELETE CASCADE
```

### Unique

For one schedule:

```text
UNIQUE(provider_id, location_id, day_of_week)
```

### Constraints

```text
day_of_week BETWEEN 0 AND 6
```

If:

```text
is_closed = true
```

then `opens_at` and `closes_at` should be NULL.

Otherwise:

```text
opens_at < closes_at
```

---

# 4.3 `provider_service_areas`

Defines where home services are offered.

| Column         | Type         | Null | Key |
| -------------- | ------------ | ---: | --- |
| `id`           | UUID         |   No | PK  |
| `provider_id`  | UUID         |   No | FK  |
| `name`         | VARCHAR(150) |   No |     |
| `postal_code`  | VARCHAR(20)  |  Yes |     |
| `city`         | VARCHAR(100) |  Yes |     |
| `state`        | VARCHAR(100) |  Yes |     |
| `country_code` | CHAR(2)      |   No |     |
| `is_active`    | BOOLEAN      |   No |     |
| `created_at`   | TIMESTAMPTZ  |   No |     |
| `updated_at`   | TIMESTAMPTZ  |   No |     |

### FK

```text
provider_id → provider_organizations.id
ON DELETE CASCADE
```

### Indexes

```text
idx_service_area_provider
idx_service_area_postal_code
idx_service_area_city
```

### Business constraint

A `HOME_SERVICE` booking must be inside a provider's active service area.

V1 can use postal-code/city validation rather than GIS polygons.

---

# 4.4 `agent_availability`

Individual agent working availability.

| Column          | Type        | Null | Key |
| --------------- | ----------- | ---: | --- |
| `id`            | UUID        |   No | PK  |
| `membership_id` | UUID        |   No | FK  |
| `day_of_week`   | SMALLINT    |   No |     |
| `start_time`    | TIME        |   No |     |
| `end_time`      | TIME        |   No |     |
| `created_at`    | TIMESTAMPTZ |   No |     |
| `updated_at`    | TIMESTAMPTZ |   No |     |

### FK

```text
membership_id → provider_memberships.id
ON DELETE CASCADE
```

### Unique

```text
UNIQUE(membership_id, day_of_week, start_time, end_time)
```

### Constraints

```text
start_time < end_time
```

Only memberships with:

```text
role = AGENT
status = ACTIVE
```

should be used for assignment.

---

# 4.5 `agent_time_off`

Agent leave/unavailability.

| Column          | Type         | Null | Key |
| --------------- | ------------ | ---: | --- |
| `id`            | UUID         |   No | PK  |
| `membership_id` | UUID         |   No | FK  |
| `start_at`      | TIMESTAMPTZ  |   No |     |
| `end_at`        | TIMESTAMPTZ  |   No |     |
| `reason`        | VARCHAR(255) |  Yes |     |
| `created_at`    | TIMESTAMPTZ  |   No |     |
| `updated_at`    | TIMESTAMPTZ  |   No |     |

### FK

```text
membership_id → provider_memberships.id
ON DELETE CASCADE
```

### Constraint

```text
start_at < end_at
```

### Index

```text
idx_agent_time_off_membership_range
```

V1 scheduling must check time-off records before assignment.

---

# 5. Service Catalog

# 5.1 `service_categories`

Platform-level service categories.

| Column        | Type         | Null | Key    |
| ------------- | ------------ | ---: | ------ |
| `id`          | UUID         |   No | PK     |
| `name`        | VARCHAR(100) |   No | Unique |
| `slug`        | VARCHAR(120) |   No | Unique |
| `description` | TEXT         |  Yes |        |
| `is_active`   | BOOLEAN      |   No |        |
| `created_at`  | TIMESTAMPTZ  |   No |        |
| `updated_at`  | TIMESTAMPTZ  |   No |        |

### Unique

```text
UNIQUE(name)
UNIQUE(slug)
```

### Index

```text
idx_service_categories_active
```

---

# 5.2 `services`

Provider-specific service offering.

| Column             | Type          | Null | Key |
| ------------------ | ------------- | ---: | --- |
| `id`               | UUID          |   No | PK  |
| `provider_id`      | UUID          |   No | FK  |
| `category_id`      | UUID          |   No | FK  |
| `name`             | VARCHAR(200)  |   No |     |
| `description`      | TEXT          |  Yes |     |
| `duration_minutes` | INTEGER       |   No |     |
| `base_price`       | NUMERIC(12,2) |   No |     |
| `currency`         | CHAR(3)       |   No |     |
| `status`           | ServiceStatus |   No |     |
| `created_at`       | TIMESTAMPTZ   |   No |     |
| `updated_at`       | TIMESTAMPTZ   |   No |     |
| `archived_at`      | TIMESTAMPTZ   |  Yes |     |

### FKs

```text
provider_id → provider_organizations.id
ON DELETE RESTRICT

category_id → service_categories.id
ON DELETE RESTRICT
```

### Indexes

```text
idx_services_provider
idx_services_category
idx_services_status
idx_services_provider_status
```

### Constraints

```text
duration_minutes > 0
base_price >= 0
```

### Business constraints

Only:

```text
status = ACTIVE
```

services can be booked.

A service cannot be physically deleted if historical bookings reference it.

---

# 5.3 `service_requirements`

Additional information required for a specific service.

| Column             | Type            | Null | Key |
| ------------------ | --------------- | ---: | --- |
| `id`               | UUID            |   No | PK  |
| `service_id`       | UUID            |   No | FK  |
| `name`             | VARCHAR(150)    |   No |     |
| `description`      | TEXT            |  Yes |     |
| `requirement_type` | RequirementType |   No |     |
| `is_required`      | BOOLEAN         |   No |     |
| `options`          | JSONB           |  Yes |     |
| `display_order`    | INTEGER         |   No |     |
| `created_at`       | TIMESTAMPTZ     |   No |     |
| `updated_at`       | TIMESTAMPTZ     |   No |     |

### FK

```text
service_id → services.id
ON DELETE CASCADE
```

### Unique

```text
UNIQUE(service_id, name)
```

### Constraints

```text
display_order >= 0
```

For select-type requirements, `options` must contain the permitted choices.

---

# 6. Booking & Scheduling

# 6.1 `bookings`

Core customer appointment/order.

| Column                | Type          | Null | Key              |
| --------------------- | ------------- | ---: | ---------------- |
| `id`                  | UUID          |   No | PK               |
| `booking_reference`   | VARCHAR(30)   |   No | Unique           |
| `customer_id`         | UUID          |   No | FK users         |
| `provider_id`         | UUID          |   No | FK organizations |
| `service_id`          | UUID          |   No | FK services      |
| `service_mode`        | ServiceMode   |   No |                  |
| `status`              | BookingStatus |   No |                  |
| `scheduled_start_at`  | TIMESTAMPTZ   |   No |                  |
| `scheduled_end_at`    | TIMESTAMPTZ   |   No |                  |
| `service_price`       | NUMERIC(12,2) |   No |                  |
| `tax_amount`          | NUMERIC(12,2) |   No |                  |
| `discount_amount`     | NUMERIC(12,2) |   No |                  |
| `total_amount`        | NUMERIC(12,2) |   No |                  |
| `currency`            | CHAR(3)       |   No |                  |
| `customer_notes`      | TEXT          |  Yes |                  |
| `provider_notes`      | TEXT          |  Yes |                  |
| `cancelled_at`        | TIMESTAMPTZ   |  Yes |                  |
| `cancelled_by`        | UUID          |  Yes | FK users         |
| `cancellation_reason` | TEXT          |  Yes |                  |
| `completed_at`        | TIMESTAMPTZ   |  Yes |                  |
| `created_at`          | TIMESTAMPTZ   |   No |                  |
| `updated_at`          | TIMESTAMPTZ   |   No |                  |

### FKs

```text
customer_id → users.id
ON DELETE RESTRICT

provider_id → provider_organizations.id
ON DELETE RESTRICT

service_id → services.id
ON DELETE RESTRICT

cancelled_by → users.id
ON DELETE SET NULL
```

### Unique

```text
UNIQUE(booking_reference)
```

### Indexes

```text
idx_bookings_customer
idx_bookings_provider
idx_bookings_service
idx_bookings_status
idx_bookings_scheduled_start
idx_bookings_provider_status
idx_bookings_customer_status
```

### Constraints

```text
scheduled_start_at < scheduled_end_at

service_price >= 0
tax_amount >= 0
discount_amount >= 0
total_amount >= 0
```

Recommended financial consistency:

```text
total_amount =
service_price + tax_amount - discount_amount
```

This should be validated in the service layer.

### Important V1 rule

There is **no provider-wide booking exclusion constraint**.

This is intentional.

Multiple agents from the same provider can have simultaneous bookings.

---

# 6.2 `booking_locations`

Actual service location.

| Column          | Type         | Null | Key |
| --------------- | ------------ | ---: | --- |
| `id`            | UUID         |   No | PK  |
| `booking_id`    | UUID         |   No | FK  |
| `address_line1` | VARCHAR(255) |   No |     |
| `address_line2` | VARCHAR(255) |  Yes |     |
| `city`          | VARCHAR(100) |   No |     |
| `state`         | VARCHAR(100) |   No |     |
| `postal_code`   | VARCHAR(20)  |   No |     |
| `country_code`  | CHAR(2)      |   No |     |
| `latitude`      | NUMERIC(9,6) |  Yes |     |
| `longitude`     | NUMERIC(9,6) |  Yes |     |
| `instructions`  | TEXT         |  Yes |     |
| `created_at`    | TIMESTAMPTZ  |   No |     |
| `updated_at`    | TIMESTAMPTZ  |   No |     |

### FK

```text
booking_id → bookings.id
ON DELETE CASCADE
```

### Unique

```text
UNIQUE(booking_id)
```

One booking has one service location.

### Business constraint

Required for:

```text
service_mode = HOME_SERVICE
```

Not required for:

```text
service_mode = AT_PROVIDER
```

---

# 6.3 `booking_assignments`

Tracks which agent is responsible for executing a booking.

This table is critical for V1 scheduling.

| Column                | Type             | Null | Key     |
| --------------------- | ---------------- | ---: | ------- |
| `id`                  | UUID             |   No | PK      |
| `booking_id`          | UUID             |   No | FK      |
| `agent_membership_id` | UUID             |   No | FK      |
| `status`              | AssignmentStatus |   No |         |
| `scheduled_start_at`  | TIMESTAMPTZ      |   No |         |
| `scheduled_end_at`    | TIMESTAMPTZ      |   No |         |
| `blocked_start_at`    | TIMESTAMPTZ      |   No |         |
| `blocked_end_at`      | TIMESTAMPTZ      |   No |         |
| `assigned_at`         | TIMESTAMPTZ      |   No |         |
| `accepted_at`         | TIMESTAMPTZ      |  Yes |         |
| `released_at`         | TIMESTAMPTZ      |  Yes |         |
| `reassigned_from_id`  | UUID             |  Yes | Self FK |
| `assignment_notes`    | TEXT             |  Yes |         |
| `created_at`          | TIMESTAMPTZ      |   No |         |
| `updated_at`          | TIMESTAMPTZ      |   No |         |

### FKs

```text
booking_id → bookings.id
ON DELETE RESTRICT

agent_membership_id → provider_memberships.id
ON DELETE RESTRICT

reassigned_from_id → booking_assignments.id
ON DELETE SET NULL
```

### Indexes

```text
idx_assignment_booking
idx_assignment_agent
idx_assignment_status
idx_assignment_agent_time
```

### Constraints

```text
scheduled_start_at < scheduled_end_at
blocked_start_at < blocked_end_at
```

### Critical scheduling constraint

For active assignments, an agent must not have overlapping blocked periods.

Conceptually:

```text
agent_membership_id
+
tstzrange(blocked_start_at, blocked_end_at)
```

with PostgreSQL exclusion logic for active assignments.

For example:

```text
status IN (
    ASSIGNED,
    ACCEPTED,
    EN_ROUTE,
    IN_PROGRESS
)
```

This is the V1 replacement for the old provider-wide booking exclusion.

### Why `blocked_start_at` / `blocked_end_at`?

For example:

```text
Service:
10:00 → 11:00

Travel/buffer:
09:30 → 11:30
```

Agent availability is blocked for the whole operational period, not merely the service duration.

---

# 6.4 `booking_status_history`

Immutable booking lifecycle history.

| Column        | Type          | Null | Key |
| ------------- | ------------- | ---: | --- |
| `id`          | UUID          |   No | PK  |
| `booking_id`  | UUID          |   No | FK  |
| `from_status` | BookingStatus |  Yes |     |
| `to_status`   | BookingStatus |   No |     |
| `changed_by`  | UUID          |  Yes | FK  |
| `reason`      | TEXT          |  Yes |     |
| `created_at`  | TIMESTAMPTZ   |   No |     |

### FKs

```text
booking_id → bookings.id
ON DELETE CASCADE

changed_by → users.id
ON DELETE SET NULL
```

### Indexes

```text
idx_booking_status_history_booking
idx_booking_status_history_created
```

This table should be treated as append-only.

---

# 6.5 `booking_travel`

Travel and operational scheduling data.

| Column                       | Type         | Null | Key       |
| ---------------------------- | ------------ | ---: | --------- |
| `id`                         | UUID         |   No | PK        |
| `booking_id`                 | UUID         |   No | FK        |
| `assignment_id`              | UUID         |  Yes | FK        |
| `travel_status`              | TravelStatus |   No |           |
| `estimated_duration_minutes` | INTEGER      |  Yes |           |
| `buffer_before_minutes`      | INTEGER      |   No | Default 0 |
| `buffer_after_minutes`       | INTEGER      |   No | Default 0 |
| `started_at`                 | TIMESTAMPTZ  |  Yes |           |
| `arrived_at`                 | TIMESTAMPTZ  |  Yes |           |
| `completed_at`               | TIMESTAMPTZ  |  Yes |           |
| `created_at`                 | TIMESTAMPTZ  |   No |           |
| `updated_at`                 | TIMESTAMPTZ  |   No |           |

### FKs

```text
booking_id → bookings.id
ON DELETE CASCADE

assignment_id → booking_assignments.id
ON DELETE SET NULL
```

### Unique

```text
UNIQUE(booking_id)
```

### Constraints

```text
estimated_duration_minutes >= 0
buffer_before_minutes >= 0
buffer_after_minutes >= 0
```

V1 does not require live GPS or route optimization.

---

# 7. Payment & Finance

# 7.1 `payments`

Represents payment attempt/lifecycle for a booking.

| Column               | Type          | Null | Key |
| -------------------- | ------------- | ---: | --- |
| `id`                 | UUID          |   No | PK  |
| `booking_id`         | UUID          |   No | FK  |
| `amount`             | NUMERIC(12,2) |   No |     |
| `currency`           | CHAR(3)       |   No |     |
| `method`             | PaymentMethod |   No |     |
| `status`             | PaymentStatus |   No |     |
| `provider_reference` | VARCHAR(255)  |  Yes |     |
| `paid_at`            | TIMESTAMPTZ   |  Yes |     |
| `failed_at`          | TIMESTAMPTZ   |  Yes |     |
| `failure_reason`     | TEXT          |  Yes |     |
| `created_at`         | TIMESTAMPTZ   |   No |     |
| `updated_at`         | TIMESTAMPTZ   |   No |     |

### FK

```text
booking_id → bookings.id
ON DELETE RESTRICT
```

### Indexes

```text
idx_payments_booking
idx_payments_status
idx_payments_provider_reference
```

### Constraints

```text
amount > 0
```

For V1 dummy payment:

```text
method = DUMMY
```

V1.1 can add real payment-provider identifiers.

---

# 7.2 `transactions`

Financial ledger.

| Column             | Type            | Null | Key    |
| ------------------ | --------------- | ---: | ------ |
| `id`               | UUID            |   No | PK     |
| `payment_id`       | UUID            |  Yes | FK     |
| `booking_id`       | UUID            |  Yes | FK     |
| `provider_id`      | UUID            |  Yes | FK     |
| `transaction_type` | TransactionType |   No |        |
| `amount`           | NUMERIC(14,2)   |   No |        |
| `currency`         | CHAR(3)         |   No |        |
| `reference`        | VARCHAR(255)    |   No | Unique |
| `metadata`         | JSONB           |  Yes |        |
| `created_at`       | TIMESTAMPTZ     |   No |        |

### FKs

```text
payment_id → payments.id
ON DELETE RESTRICT

booking_id → bookings.id
ON DELETE RESTRICT

provider_id → provider_organizations.id
ON DELETE RESTRICT
```

### Unique

```text
UNIQUE(reference)
```

### Indexes

```text
idx_transactions_payment
idx_transactions_booking
idx_transactions_provider
idx_transactions_type
```

Treat this as a financial history/ledger.

Do not update old transaction amounts.

---

# 7.3 `refunds`

Money returned to the customer.

| Column               | Type          | Null | Key |
| -------------------- | ------------- | ---: | --- |
| `id`                 | UUID          |   No | PK  |
| `payment_id`         | UUID          |   No | FK  |
| `booking_id`         | UUID          |   No | FK  |
| `amount`             | NUMERIC(12,2) |   No |     |
| `currency`           | CHAR(3)       |   No |     |
| `status`             | RefundStatus  |   No |     |
| `reason`             | TEXT          |  Yes |     |
| `provider_reference` | VARCHAR(255)  |  Yes |     |
| `processed_at`       | TIMESTAMPTZ   |  Yes |     |
| `created_at`         | TIMESTAMPTZ   |   No |     |
| `updated_at`         | TIMESTAMPTZ   |   No |     |

### FKs

```text
payment_id → payments.id
ON DELETE RESTRICT

booking_id → bookings.id
ON DELETE RESTRICT
```

### Constraints

```text
amount > 0
```

Application logic must prevent:

```text
total_refunded > original_payment_amount
```

---

# 7.4 `invoices`

Customer billing document.

| Column            | Type          | Null | Key    |
| ----------------- | ------------- | ---: | ------ |
| `id`              | UUID          |   No | PK     |
| `booking_id`      | UUID          |   No | FK     |
| `invoice_number`  | VARCHAR(50)   |   No | Unique |
| `customer_id`     | UUID          |   No | FK     |
| `provider_id`     | UUID          |   No | FK     |
| `subtotal`        | NUMERIC(12,2) |   No |        |
| `tax_amount`      | NUMERIC(12,2) |   No |        |
| `discount_amount` | NUMERIC(12,2) |   No |        |
| `total_amount`    | NUMERIC(12,2) |   No |        |
| `currency`        | CHAR(3)       |   No |        |
| `status`          | InvoiceStatus |   No |        |
| `issued_at`       | TIMESTAMPTZ   |  Yes |        |
| `due_at`          | TIMESTAMPTZ   |  Yes |        |
| `paid_at`         | TIMESTAMPTZ   |  Yes |        |
| `created_at`      | TIMESTAMPTZ   |   No |        |
| `updated_at`      | TIMESTAMPTZ   |   No |        |

### FKs

```text
booking_id → bookings.id
ON DELETE RESTRICT

customer_id → users.id
ON DELETE RESTRICT

provider_id → provider_organizations.id
ON DELETE RESTRICT
```

### Unique

```text
UNIQUE(invoice_number)
```

### Optional V1 rule

Normally:

```text
UNIQUE(booking_id)
```

because V1 has one invoice per booking.

---

# 7.5 `provider_settlements`

Money owed/paid to a provider.

| Column              | Type             | Null | Key |
| ------------------- | ---------------- | ---: | --- |
| `id`                | UUID             |   No | PK  |
| `provider_id`       | UUID             |   No | FK  |
| `period_start`      | DATE             |   No |     |
| `period_end`        | DATE             |   No |     |
| `gross_amount`      | NUMERIC(14,2)    |   No |     |
| `commission_amount` | NUMERIC(14,2)    |   No |     |
| `adjustment_amount` | NUMERIC(14,2)    |   No |     |
| `net_amount`        | NUMERIC(14,2)    |   No |     |
| `currency`          | CHAR(3)          |   No |     |
| `status`            | SettlementStatus |   No |     |
| `paid_at`           | TIMESTAMPTZ      |  Yes |     |
| `created_at`        | TIMESTAMPTZ      |   No |     |
| `updated_at`        | TIMESTAMPTZ      |   No |     |

### FK

```text
provider_id → provider_organizations.id
ON DELETE RESTRICT
```

### Constraints

```text
period_start <= period_end

gross_amount >= 0
commission_amount >= 0
net_amount >= 0
```

Application logic:

```text
net_amount =
gross_amount
- commission_amount
+ adjustment_amount
```

---

# 8. Customer Experience

# 8.1 `reviews`

Customer feedback about completed service.

| Column        | Type         | Null | Key |
| ------------- | ------------ | ---: | --- |
| `id`          | UUID         |   No | PK  |
| `booking_id`  | UUID         |   No | FK  |
| `customer_id` | UUID         |   No | FK  |
| `provider_id` | UUID         |   No | FK  |
| `rating`      | SMALLINT     |   No |     |
| `title`       | VARCHAR(150) |  Yes |     |
| `comment`     | TEXT         |  Yes |     |
| `status`      | ReviewStatus |   No |     |
| `created_at`  | TIMESTAMPTZ  |   No |     |
| `updated_at`  | TIMESTAMPTZ  |   No |     |

### FKs

```text
booking_id → bookings.id
ON DELETE RESTRICT

customer_id → users.id
ON DELETE RESTRICT

provider_id → provider_organizations.id
ON DELETE RESTRICT
```

### Unique

```text
UNIQUE(booking_id)
```

### Constraint

```text
rating BETWEEN 1 AND 5
```

### Business constraint

Review can only be created when:

```text
booking.status = COMPLETED
```

The customer must own the booking.

---

# 8.2 `service_issues`

Operational problem associated with a service.

| Column             | Type               | Null | Key |
| ------------------ | ------------------ | ---: | --- |
| `id`               | UUID               |   No | PK  |
| `booking_id`       | UUID               |   No | FK  |
| `reported_by`      | UUID               |   No | FK  |
| `issue_type`       | VARCHAR(100)       |   No |     |
| `description`      | TEXT               |   No |     |
| `status`           | ServiceIssueStatus |   No |     |
| `resolution_notes` | TEXT               |  Yes |     |
| `resolved_by`      | UUID               |  Yes | FK  |
| `resolved_at`      | TIMESTAMPTZ        |  Yes |     |
| `created_at`       | TIMESTAMPTZ        |   No |     |
| `updated_at`       | TIMESTAMPTZ        |   No |     |

### FKs

```text
booking_id → bookings.id
ON DELETE RESTRICT

reported_by → users.id
ON DELETE RESTRICT

resolved_by → users.id
ON DELETE SET NULL
```

### Indexes

```text
idx_service_issues_booking
idx_service_issues_status
idx_service_issues_reported_by
```

A booking can have multiple issues.

---

# 8.3 `disputes`

Formal customer/provider dispute.

| Column        | Type          | Null | Key |
| ------------- | ------------- | ---: | --- |
| `id`          | UUID          |   No | PK  |
| `booking_id`  | UUID          |   No | FK  |
| `opened_by`   | UUID          |   No | FK  |
| `reason`      | TEXT          |   No |     |
| `status`      | DisputeStatus |   No |     |
| `resolution`  | TEXT          |  Yes |     |
| `resolved_by` | UUID          |  Yes | FK  |
| `resolved_at` | TIMESTAMPTZ   |  Yes |     |
| `created_at`  | TIMESTAMPTZ   |   No |     |
| `updated_at`  | TIMESTAMPTZ   |   No |     |

### FKs

```text
booking_id → bookings.id
ON DELETE RESTRICT

opened_by → users.id
ON DELETE RESTRICT

resolved_by → users.id
ON DELETE SET NULL
```

### Indexes

```text
idx_disputes_booking
idx_disputes_status
idx_disputes_opened_by
```

A dispute is different from a normal service issue.

---

# 9. Platform / Administration

# 9.1 `notifications`

User-facing notification records.

| Column               | Type               | Null | Key |
| -------------------- | ------------------ | ---: | --- |
| `id`                 | UUID               |   No | PK  |
| `user_id`            | UUID               |   No | FK  |
| `type`               | NotificationType   |   No |     |
| `title`              | VARCHAR(200)       |   No |     |
| `message`            | TEXT               |   No |     |
| `status`             | NotificationStatus |   No |     |
| `related_booking_id` | UUID               |  Yes | FK  |
| `read_at`            | TIMESTAMPTZ        |  Yes |     |
| `created_at`         | TIMESTAMPTZ        |   No |     |

### FKs

```text
user_id → users.id
ON DELETE CASCADE

related_booking_id → bookings.id
ON DELETE SET NULL
```

### Indexes

```text
idx_notifications_user
idx_notifications_user_status
idx_notifications_booking
idx_notifications_created
```

---

# 9.2 `audit_logs`

Security/admin/important operational history.

| Column          | Type         | Null | Key |
| --------------- | ------------ | ---: | --- |
| `id`            | UUID         |   No | PK  |
| `actor_user_id` | UUID         |  Yes | FK  |
| `action`        | VARCHAR(100) |   No |     |
| `entity_type`   | VARCHAR(100) |   No |     |
| `entity_id`     | UUID         |  Yes |     |
| `request_id`    | UUID         |  Yes |     |
| `track_id`      | UUID         |  Yes |     |
| `ip_address`    | INET         |  Yes |     |
| `metadata`      | JSONB        |  Yes |     |
| `created_at`    | TIMESTAMPTZ  |   No |     |

### FK

```text
actor_user_id → users.id
ON DELETE SET NULL
```

### Indexes

```text
idx_audit_logs_actor
idx_audit_logs_entity
idx_audit_logs_action
idx_audit_logs_created
idx_audit_logs_request_id
idx_audit_logs_track_id
```

### Important rule

Audit logs are append-only.

Do not update or delete them through normal application operations.

---

# 9.3 `provider_verifications`

Admin/provider verification history.

| Column        | Type               | Null | Key |
| ------------- | ------------------ | ---: | --- |
| `id`          | UUID               |   No | PK  |
| `provider_id` | UUID               |   No | FK  |
| `reviewed_by` | UUID               |  Yes | FK  |
| `status`      | VerificationStatus |   No |     |
| `documents`   | JSONB              |  Yes |     |
| `notes`       | TEXT               |  Yes |     |
| `reviewed_at` | TIMESTAMPTZ        |  Yes |     |
| `expires_at`  | TIMESTAMPTZ        |  Yes |     |
| `created_at`  | TIMESTAMPTZ        |   No |     |

### FKs

```text
provider_id → provider_organizations.id
ON DELETE RESTRICT

reviewed_by → users.id
ON DELETE SET NULL
```

### Indexes

```text
idx_provider_verifications_provider
idx_provider_verifications_status
idx_provider_verifications_reviewer
```

### Business rule

Provider can become operational only after appropriate verification:

```text
verification.status = APPROVED
```

---

# 10. Relationship Overview

The resulting database relationship is:

```text
users
 │
 ├───────────────┐
 │               │
 ▼               ▼
provider_memberships
 │               provider_organizations
 │                       │
 │                       ├── provider_locations
 │                       ├── provider_operating_hours
 │                       ├── provider_service_areas
 │                       ├── services
 │                       │     └── service_requirements
 │                       └── provider_verifications
 │
 ├── agent_availability
 └── agent_time_off


users
 │
 └── bookings
       │
       ├── booking_locations
       ├── booking_assignments
       │       └── agent membership
       │
       ├── booking_status_history
       ├── booking_travel
       │
       ├── payments
       │     ├── transactions
       │     └── refunds
       │
       ├── invoices
       ├── reviews
       ├── service_issues
       ├── disputes
       └── notifications


provider_organizations
 │
 └── provider_settlements


users
 │
 └── audit_logs
```

---

# 11. Most Important V1 Business Constraints

The database alone cannot safely enforce every business rule. These rules belong in the service layer, with database constraints used where practical.

## 11.1 Provider activation

Provider must satisfy:

```text
Provider status = ACTIVE
AND
Provider verification = APPROVED
```

before accepting normal bookings.

---

## 11.2 Service activation

A service can be booked only when:

```text
service.status = ACTIVE
provider.status = ACTIVE
```

---

## 11.3 Agent assignment

An agent must:

```text
membership.role = AGENT
membership.status = ACTIVE
```

and belong to the same provider as the booking.

---

## 11.4 Agent availability

Before assigning:

```text
booking time
⊆ agent availability
```

and:

```text
booking time
∉ agent time off
```

and:

```text
blocked booking range
does not overlap another active assignment
```

---

## 11.5 Multi-agent provider

This must be allowed:

```text
Provider A

09:00
 ├── Agent 1 → Booking X
 ├── Agent 2 → Booking Y
 └── Agent 3 → Booking Z
```

Therefore:

```text
NO provider-wide booking exclusion constraint
```

---

## 11.6 Reassignment

When an agent changes:

```text
old assignment
    ↓
status = REASSIGNED

new assignment
    ↓
reassigned_from_id = old_assignment.id
```

Never simply overwrite the old assignment.

This preserves the operational history.

---

## 11.7 Booking status transitions

Recommended V1 transitions:

```text
PENDING
   ↓
CONFIRMED
   ↓
ASSIGNMENT_PENDING
   ↓
ASSIGNED
   ↓
IN_PROGRESS
   ↓
COMPLETED
```

Alternative paths:

```text
PENDING → CANCELLED
CONFIRMED → CANCELLED
ASSIGNED → RESCHEDULED
ASSIGNED → CANCELLED
IN_PROGRESS → COMPLETED
```

`DISPUTED` is an exceptional state and should not be treated as the normal completion path.

---

## 11.8 Payment requirement

For a paid booking:

```text
payment.status = PAID
```

before the booking becomes fully confirmed, unless the business rule explicitly permits post-service payment.

V1 dummy payment can simulate:

```text
DUMMY → PAID
```

without integrating a real payment provider.

---

## 11.9 Review

A customer may review a booking only if:

```text
booking.customer_id = current_user.id
AND
booking.status = COMPLETED
```

and:

```text
review does not already exist for booking
```

---

## 11.10 Home-service booking

For:

```text
service_mode = HOME_SERVICE
```

the booking must have:

```text
booking_location
```

and the address must be inside the provider's service area.

---

## 11.11 Provider-location booking

For:

```text
service_mode = AT_PROVIDER
```

the booking must reference an appropriate provider location.

V1 can validate this at the service layer rather than adding a separate booking-location-type column.

---

# 12. Index Strategy

Do not index every column.

The important V1 indexes are based primarily on:

```text
foreign keys
status filtering
date/time queries
lookup/reference values
```

Especially:

```text
users(email)

provider_memberships(provider_id, user_id)
provider_memberships(user_id)

services(provider_id, status)
services(category_id)

bookings(customer_id, status)
bookings(provider_id, status)
bookings(scheduled_start_at)

booking_assignments(agent_membership_id, status)
booking_assignments(agent_membership_id, blocked_start_at, blocked_end_at)

payments(booking_id, status)

transactions(provider_id)
transactions(booking_id)

notifications(user_id, status)

audit_logs(entity_type, entity_id)
audit_logs(request_id)
```

---

# 13. Tables That Should Be Append-Only / Historical

The following should generally never be edited destructively:

```text
booking_status_history
booking_assignments
transactions
refunds
audit_logs
provider_verifications
```

Instead of:

```text
UPDATE old history
```

create a new record representing the new event/state.

---

# 14. Tables That Prefer Soft Deactivation

These should normally remain in the database:

```text
users
provider_organizations
provider_memberships
provider_locations
services
service_categories
```

Use fields such as:

```text
status
is_active
deactivated_at
archived_at
```

rather than physical deletion.

This is important because historical bookings may depend on these records.

---

# 15. V1.0.0 Table Count

The final V1 baseline remains exactly **27 tables**:

### Identity & Provider

1. `users`
2. `provider_organizations`
3. `provider_memberships`

### Provider Operations

4. `provider_locations`
5. `provider_operating_hours`
6. `provider_service_areas`
7. `agent_availability`
8. `agent_time_off`

### Service Catalog

9. `service_categories`
10. `services`
11. `service_requirements`

### Booking & Scheduling

12. `bookings`
13. `booking_locations`
14. `booking_assignments`
15. `booking_status_history`
16. `booking_travel`

### Payments & Finance

17. `payments`
18. `transactions`
19. `refunds`
20. `invoices`
21. `provider_settlements`

### Customer Experience

22. `reviews`
23. `service_issues`
24. `disputes`

### Platform / Administration

25. `notifications`
26. `audit_logs`
27. `provider_verifications`

---

# 16. Deliberate V1 Omissions

The following are intentionally **not** separate tables in V1:

```text
customer_profiles
agent_profiles
provider_branches
service_modes
booking_items
payment_methods
payment_webhooks
coupons
promotions
wallets
payout_accounts
chat_messages
live_location
route_optimization
calendar_integrations
subscription_plans
```

This keeps V1 as a realistic modular monolith rather than turning it into an unnecessarily large enterprise system.

Some may become V1.1/V2 domains.

---

# 17. Migration Strategy

The V0.0.1 → V1.0.0 migration should **not** be one giant blind autogenerate operation.

The old tables:

```text
provider_profiles
availability
bookings
```

have structural changes that affect the domain model.

The migration should therefore be handled deliberately.

Conceptually:

```text
V0.0.1
   │
   ├── users
   ├── provider_profiles
   ├── availability
   ├── services
   ├── bookings
   ├── reviews
   ├── notifications
   ├── audit_logs
   └── service_categories
             │
             ▼
        V1.0.0 migration
             │
             ├── provider_organizations
             ├── provider_memberships
             ├── provider_locations
             ├── provider_operating_hours
             ├── provider_service_areas
             ├── agent_availability
             ├── agent_time_off
             ├── expanded services
             ├── expanded bookings
             ├── booking_locations
             ├── booking_assignments
             ├── booking_status_history
             ├── booking_travel
             ├── payments
             ├── transactions
             ├── refunds
             ├── invoices
             ├── provider_settlements
             ├── service_issues
             ├── disputes
             └── provider_verifications
```

The existing data should be mapped into the new structure where possible rather than automatically discarded.

---

# 18. Final V1 Design Principle

The most important structural change from V0.0.1 is:

```text
V0.0.1

User
 └── ProviderProfile
       └── Availability
             └── Booking
```

becomes:

```text
V1.0.0

User
 ├── Customer
 │
 └── ProviderMembership
       │
       ▼
ProviderOrganization
 ├── Locations
 ├── OperatingHours
 ├── ServiceAreas
 ├── Services
 │    └── Requirements
 └── Agents
      ├── Availability
      ├── TimeOff
      └── BookingAssignments
                │
                ▼
             Booking
             ├── Location
             ├── Travel
             ├── StatusHistory
             ├── Payment
             │    ├── Transactions
             │    └── Refunds
             ├── Invoice
             ├── Review
             ├── Issues
             └── Disputes
```

This gives ServiceHub a database model capable of supporting the intended real-world workflow while remaining a **single modular application** rather than prematurely introducing microservices or other unnecessary infrastructure.
