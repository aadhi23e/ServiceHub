# Alembic Migration Setup Guide

## Overview
This project uses **Alembic** for database schema versioning and **SQLAlchemy** as the ORM. PostgreSQL is your database.

---

## Quick Start: Create Tables from Scratch

### 1. Initialize the Database Connection
The `backend` container runs with `docker-compose.yml` which:
- Connects to PostgreSQL at `postgres:5432` (inside Docker network)
- Uses database name `servicehub`
- Loads credentials from `backend/.env.docker`

Ensure your `.env.docker` has:
```
DATABASE_URL=postgresql://servicehub:servicehub@postgres:5432/servicehub
```

### 2. Create Initial Migration

Run this command inside the backend container to generate a migration from your existing SQLAlchemy models:

```bash
docker exec servicehub-backend alembic revision --autogenerate -m "Initial schema"
```

This scans your `app/models/` directory and creates a migration file in `migrations/versions/`.

### 3. Apply the Migration

Apply the migration to create all tables in PostgreSQL:

```bash
docker exec servicehub-backend alembic upgrade head
```

This runs all pending migrations and creates:
- `user` table
- `address` table
- `booking` table
- `payment` table
- `dispute` table
- `invoice` table
- `notification` table
- `review` table
- `service` table
- `service_category` table
- `transaction` table
- `audit_log` table
- And all other tables defined in `app/models/`

---

## Common Alembic Commands

### View Current Migration Status
```bash
docker exec servicehub-backend alembic current
```

### View Migration History
```bash
docker exec servicehub-backend alembic history --verbose
```

### Rollback One Migration
```bash
docker exec servicehub-backend alembic downgrade -1
```

### Rollback to a Specific Migration
```bash
docker exec servicehub-backend alembic downgrade <revision_id>
```

### Create a Manual Migration (without autogenerate)
```bash
docker exec servicehub-backend alembic revision -m "Add new column to users"
```
Then edit the migration file in `migrations/versions/` to write SQL manually.

---

## How Alembic Works

### Migration Lifecycle
1. **Create** → `alembic revision --autogenerate -m "message"` generates a migration file
2. **Review** → Check the file in `migrations/versions/`
3. **Apply** → `alembic upgrade head` runs all pending migrations
4. **Rollback** → `alembic downgrade <rev>` reverts changes

### Auto-Generated Migrations
When you run `alembic revision --autogenerate`:
- Alembic compares your SQLAlchemy models with the current database schema
- It generates Python code to create tables, columns, constraints, indexes
- The migration is **idempotent** and **reversible**

### Workflow Example
```bash
# 1. Modify app/models/user.py (e.g., add a `phone` column)
# 2. Generate migration
docker exec servicehub-backend alembic revision --autogenerate -m "Add phone to user"

# 3. Review the generated file (appears in migrations/versions/)
# 4. Apply it
docker exec servicehub-backend alembic upgrade head

# 5. Verify the schema
docker exec servicehub-postgres psql -U servicehub -d servicehub -c "\dt"
```

---

## Current Models in Your Project

Your `app/models/` directory contains:
- `user.py` → Users (customers, providers)
- `address.py` → User/Provider addresses
- `booking.py` → Service bookings
- `booking_assignment.py` → Agent/Provider assigned to booking
- `booking_location.py` → Pickup/Dropoff locations
- `booking_status_history.py` → Booking status timeline
- `booking_travel.py` → Travel details for bookings
- `payment.py` → Payment records
- `dispute.py` → Dispute/Complaint records
- `invoice.py` → Invoice records
- `notification.py` → Notification logs
- `review.py` → User reviews
- `service.py` → Service offerings
- `service_category.py` → Service categories
- `transaction.py` → Financial transactions
- `audit_log.py` → Audit trail
- `provider_profile.py` → Provider profiles
- `provider_organization.py` → Organization info
- `provider_service_area.py` → Service areas
- `provider_location.py` → Provider locations
- `provider_membership.py` → Membership records
- `provider_operating_hours.py` → Operating hours
- `provider_verification.py` → Verification status
- `provider_settlement.py` → Settlement records
- `service_issue.py` → Service issues/complaints
- `service_requirement.py` → Service requirements
- `user_address.py` → User address relationships
- `agent_availability.py` → Agent availability schedules
- `agent_time_off.py` → Agent time off records
- `refund.py` → Refund records

---

## Troubleshooting

### Migration Already Applied
If you see `"Target database is not up to date"`, run:
```bash
docker exec servicehub-backend alembic upgrade head
```

### Database Connection Error
Check PostgreSQL is running:
```bash
docker ps | grep postgres
```

Verify credentials in `backend/.env.docker`:
```bash
docker exec servicehub-postgres psql -U servicehub -d servicehub -c "SELECT 1"
```

### Models Not Being Detected
Ensure all model files are imported in `app/models/__init__.py`:
```python
from app.models.user import User
from app.models.address import Address
from app.models.booking import Booking
# ... etc
```

Alembic reads `target_metadata = Base.metadata` from `migrations/env.py`, which includes all models imported in the app.

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `alembic revision --autogenerate -m "msg"` | Generate migration from models |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Rollback last migration |
| `alembic history --verbose` | Show all migrations |
| `alembic current` | Show current migration |
| `alembic stamp head` | Mark current state as up-to-date (skip migrations) |

---

## Next Steps

1. **Generate initial migration:**
   ```bash
   docker exec servicehub-backend alembic revision --autogenerate -m "Initial schema"
   ```

2. **Apply it:**
   ```bash
   docker exec servicehub-backend alembic upgrade head
   ```

3. **Verify tables were created:**
   ```bash
   docker exec servicehub-postgres psql -U servicehub -d servicehub -c "\dt"
   ```

4. **Start developing** — Future model changes → generate migrations → apply them.
