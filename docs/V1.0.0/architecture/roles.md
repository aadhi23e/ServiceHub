Yes. **This is the architecture decision we should settle now.** Your idea is workable, but I would make a few important changes so the model stays simple without creating problems later.

The key distinction should be:

> **Platform role = what kind of account/person this is on ServiceHub.**
> **Provider membership role = what authority that person has inside a particular provider organization.**

That gives us a clean two-level role system.

---

# 1. The identity model I recommend for ServiceHub V1

```text
                         ┌──────────────────┐
                         │       User       │
                         │                  │
                         │ platform_role    │
                         │ CUSTOMER         │
                         │ PROVIDER         │
                         │ ADMIN            │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
         Customer use       Provider Membership    Admin use
                              │
                              ▼
                    ┌─────────────────────┐
                    │ ProviderOrganization│
                    │                     │
                    │ Company / Shop      │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
              OWNER         MANAGER        AGENT
                                             │
                                             ▼
                                       Agent Type
```

So there are **two different role concepts**:

### Platform role

Stored on `users`.

```text
CUSTOMER
PROVIDER
ADMIN
```

This answers:

> "What is this account primarily using ServiceHub as?"

### Organization role

Stored on `provider_memberships`.

```text
OWNER
MANAGER
AGENT
```

This answers:

> "What can this user do inside this particular provider organization?"

This is much cleaner than putting `OWNER`, `MANAGER`, `AGENT` directly into `users.role`.

---

# 2. One important correction to your idea

You said:

> "roles can be users.roles which will tell what the user is"

Yes, **but don't make the platform role the complete authorization system.**

For example:

```text
User A
platform_role = PROVIDER

Provider Organization A
membership_role = OWNER
```

Another:

```text
User B
platform_role = PROVIDER

Provider Organization A
membership_role = MANAGER
```

Another:

```text
User C
platform_role = PROVIDER

Provider Organization A
membership_role = AGENT
```

The `users.role` says:

```text
This is a provider-side account.
```

The membership says:

```text
This provider-side account is an OWNER/MANAGER/AGENT
of this particular organization.
```

That's the separation we want.

---

# 3. A customer becoming a provider

This part of your idea is actually very good.

A person can initially register normally:

```text
Register
   ↓
User
platform_role = CUSTOMER
   ↓
Use ServiceHub
   ↓
"Become a Provider"
   ↓
Create Provider Organization
```

Then:

```text
Provider Organization
        │
        └── Provider Membership
                │
                ├── user_id = current user
                └── role = OWNER
```

And the user's platform role becomes:

```text
PROVIDER
```

But **this does not mean they stop being capable of acting as a customer**.

For example:

```text
User
 ├── platform_role = PROVIDER
 │
 ├── Provider Organization
 │      └── OWNER
 │
 └── Customer bookings
       ├── Booked electrician
       └── Booked cleaning service
```

That is important.

A provider owner should still be able to book another ServiceHub provider for themselves.

---

# 4. Direct provider registration

You also proposed:

> They can directly register as a provider without first creating a customer account.

I agree.

We should support **two entry points**, but both eventually create the same underlying objects.

### Flow A — Existing customer becomes provider

```text
Login
  ↓
Customer Dashboard
  ↓
Become a Provider
  ↓
Provider Organization Registration
  ↓
Organization created
  ↓
Membership created
role = OWNER
  ↓
Verification
  ↓
Approved
  ↓
Provider Dashboard
```

### Flow B — New provider registration

```text
Provider Registration
  ↓
Create User
platform_role = PROVIDER
  ↓
Create Provider Organization
  ↓
Create OWNER membership
  ↓
Verification
  ↓
Approved
  ↓
Provider Dashboard
```

The important part is:

**Both flows converge to exactly the same database structure.**

We don't want two different provider architectures.

---

# 5. Provider organization creation

I would define it like this:

```text
User
  │
  │ creates
  ▼
ProviderOrganization
  │
  ├── name
  ├── business details
  ├── status = PENDING
  ├── created_by
  │
  └── ProviderMembership
          │
          ├── user_id
          ├── organization_id
          ├── role = OWNER
          └── status = ACTIVE
```

The creator automatically becomes:

```text
OWNER
```

They don't need to separately add themselves.

---

# 6. Verification

Your idea that the company/shop should be reviewed before becoming fully operational is also correct.

Initially:

```text
ProviderOrganization.status = PENDING
```

Then admin reviews it.

```text
PENDING
   │
   ├── APPROVED → ACTIVE
   │
   └── REJECTED
```

Only after approval should the organization be allowed to accept normal bookings.

So:

```text
OWNER creates organization
        ↓
Organization = PENDING
        ↓
Admin verification
        ↓
APPROVED
        ↓
Organization = ACTIVE
        ↓
Services can become bookable
```

---

# 7. How should adding a Manager/Agent work?

This is where I would **change your proposed approach**.

You said:

> owner/manager will generate Gmail and register that and give it to the user

I would **not have ServiceHub create Gmail accounts**.

ServiceHub should not create external Gmail accounts.

Instead:

```text
OWNER / MANAGER
      ↓
Add team member
      ↓
Enter person's existing email
      ↓
Select role
      ↓
AGENT / MANAGER
      ↓
ServiceHub sends invitation
      ↓
Person clicks invitation
      ↓
Creates/sets their password
      ↓
Account activated
      ↓
Membership activated
```

For example:

```text
Owner:
"Add Agent"

Email:
agent123@gmail.com

Role:
AGENT

Agent Type:
MOBILE

        ↓

Invitation email
        ↓

agent123@gmail.com
        ↓

Set password
        ↓

Login
        ↓

Provider Agent Dashboard
```

This is much safer than an owner knowing another employee's password.

---

# 8. What happens if the invited email already has a ServiceHub account?

This is another reason the invitation model is useful.

Suppose:

```text
john@gmail.com
```

already has a customer account.

The owner adds:

```text
john@gmail.com
role = AGENT
```

We don't create another User.

Instead:

```text
Existing User
     │
     ├── Customer usage
     │
     └── Provider Membership
             │
             └── AGENT
```

So **one email = one User account**.

That's an important architectural rule.

---

# 9. What if the user doesn't have a ServiceHub account?

Then:

```text
Owner
  ↓
Invite email
  ↓
Invitation
  ↓
User accepts
  ↓
Creates ServiceHub account
  ↓
Membership automatically connected
```

So we don't need:

```text
Create temporary account
Create temporary password
Give password to employee
```

Instead:

```text
Invitation → account creation → membership activation
```

Much cleaner.

---

# 10. What roles can a provider organization have?

For V1:

```text
OWNER
MANAGER
AGENT
```

### OWNER

Can:

* manage organization
* manage branches
* manage services
* manage managers
* manage agents
* manage bookings
* view financial information
* handle provider settings

### MANAGER

Can:

* manage bookings
* manage agents
* assign agents
* manage schedules
* manage services
* manage operational information

But cannot perform owner-only actions such as transferring ownership or deleting the organization.

### AGENT

Can:

* see assigned bookings
* accept/decline assignments
* update travel status
* start service
* complete service
* view relevant customer/service information

The exact permission matrix can be finalized later.

---

# 11. Your "what kind of agent?" question

This is an important distinction.

Don't put something like:

```text
role = MOBILE_AGENT
```

because then role and job type become mixed together.

Instead:

```text
membership_role = AGENT

agent_type = MOBILE
```

For V1 I would keep it simple:

```text
AgentType

MOBILE
ON_SITE
HYBRID
```

Meaning:

### MOBILE

Primarily performs home/customer-location services.

```text
Customer
   ↑
Agent travels to customer
```

### ON_SITE

Primarily works at provider locations.

```text
Customer
   ↓
Provider branch
   ↓
Agent
```

### HYBRID

Can do both.

```text
Customer location
        OR
Provider location
```

But there is an even more important point:

**Agent type should not be the thing that ultimately decides whether an agent can perform a service.**

The actual scheduling decision should eventually consider:

```text
Agent
+
Service
+
Service mode
+
Availability
+
Time off
+
Existing assignments
+
Location/travel
```

So `agent_type` is a useful profile/capability field, not the entire scheduling system.

---

# 12. One organization can have multiple branches

Yes.

Your requirement:

> one company but multiple branches

should be represented as:

```text
ProviderOrganization
        │
        ├── ProviderLocation
        │      └── Chennai Branch
        │
        ├── ProviderLocation
        │      └── Bangalore Branch
        │
        └── ProviderLocation
               └── Coimbatore Branch
```

So:

```text
ONE ORGANIZATION
      │
      ├── LOCATION 1
      ├── LOCATION 2
      ├── LOCATION 3
      └── LOCATION N
```

Not:

```text
Company 1
Company 2
Company 3
```

unless the owner actually creates separate businesses.

---

# 13. Address architecture

Here I would make another important correction.

Don't make one generic `address` field inside `users` and another inside `provider_organizations`.

Instead, create an actual:

```text
addresses
```

table.

Then connect addresses to their owners.

A clean V1 structure is:

```text
                    addresses
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
          User                 Provider
       addresses             locations
```

More specifically:

```text
User
 │
 └── UserAddress
       │
       └── Address
```

and:

```text
ProviderOrganization
 │
 └── ProviderLocation
       │
       └── Address
```

This means:

### Customer

```text
User
 ├── Address
 │     └── Home
 │
 ├── Address
 │     └── Work
 │
 └── Address
       └── Parents
```

### Provider

```text
ProviderOrganization
 │
 ├── ProviderLocation
 │      └── Address
 │
 ├── ProviderLocation
 │      └── Address
 │
 └── ProviderLocation
        └── Address
```

This gives us exactly what you described.

---

# 14. Don't connect booking directly to the user's address

This is very important.

Suppose:

```text
Customer Address

Home
123 ABC Street
```

They create a booking.

We copy the relevant address information into:

```text
booking_locations
```

So:

```text
UserAddress
     ↓
Booking
     ↓
BookingLocation
```

The booking location becomes a **historical snapshot**.

Why?

Because six months later the customer might change:

```text
Home
123 ABC Street
```

to:

```text
Home
456 XYZ Street
```

The old booking must still say:

```text
Service was performed at:
123 ABC Street
```

not suddenly change to the customer's new address.

So this separation is essential.

---

# 15. The final identity architecture

I recommend freezing V1 around this:

```text
                         USER
                          │
              ┌───────────┼────────────┐
              │           │            │
              ▼           ▼            ▼
          CUSTOMER     PROVIDER      ADMIN
              │           │
              │           │
              │           ▼
              │     PROVIDER ORGANIZATION
              │             │
              │             ├── Locations
              │             ├── Services
              │             ├── Service Areas
              │             ├── Operating Hours
              │             │
              │             └── Memberships
              │                    │
              │          ┌─────────┼─────────┐
              │          │         │         │
              │        OWNER     MANAGER    AGENT
              │                              │
              │                              ▼
              │                         Agent Type
              │
              └── User Addresses
```

And the relationships:

```text
User
 ├── addresses
 ├── customer_bookings
 ├── provider_memberships
 ├── notifications
 ├── reviews
 └── ...

ProviderOrganization
 ├── locations
 ├── services
 ├── service_areas
 ├── operating_hours
 ├── memberships
 └── verifications

ProviderMembership
 ├── user_id
 ├── organization_id
 ├── role
 ├── status
 └── agent_type (nullable; only meaningful for AGENT)
```

---

# 16. The registration flows after this decision

## Customer

```text
Register
   ↓
User
role = CUSTOMER
   ↓
Customer Dashboard
```

---

## New provider

```text
Provider Registration
       ↓
Create User
role = PROVIDER
       ↓
Create Organization
       ↓
Create OWNER Membership
       ↓
Add organization address/location
       ↓
Submit verification
       ↓
PENDING
       ↓
Admin approval
       ↓
ACTIVE
       ↓
Provider Dashboard
```

---

## Existing customer becomes provider

```text
Customer
   ↓
Become Provider
   ↓
Create Organization
   ↓
User.role = PROVIDER
   ↓
Create OWNER membership
   ↓
Verification
   ↓
Approval
   ↓
Provider Dashboard
```

---

## Owner adds manager

```text
Owner
 ↓
Add Member
 ↓
Email
 ↓
MANAGER
 ↓
Invitation
 ↓
User accepts
 ↓
Provider Membership
role = MANAGER
```

---

## Owner/manager adds agent

```text
Owner / Manager
       ↓
Add Member
       ↓
Email
       ↓
Role = AGENT
       ↓
Agent Type = MOBILE / ON_SITE / HYBRID
       ↓
Invitation
       ↓
User accepts
       ↓
Provider Membership
```

---

# 17. One more decision: should one user be allowed to belong to multiple companies?

Your current requirement says:

> one user can only have company but can have multiple branches

For **V1**, we can enforce:

```text
One user → one owned provider organization
```

But I strongly recommend **not designing the database in a way that makes multiple memberships impossible**.

For example:

```text
provider_memberships

user_id
organization_id
role
status
```

should naturally support:

```text
User A
 ├── Organization A → OWNER
 └── Organization B → AGENT
```

even if our V1 business rule doesn't expose that functionality.

That gives us flexibility without adding another complicated system.

---

# 18. What I would NOT build right now

To keep V1 realistic and avoid overengineering, I would **not** introduce:

```text
roles table
permissions table
role_permissions table
teams
team_members
organization_roles
organization_permissions
```

The V1 authorization model can simply be:

```text
users.role
+
provider_memberships.role
+
centralized backend permission rules
```

That is enough for the application we are building.

Later, if ServiceHub genuinely needs custom organization roles, then we can introduce a more dynamic RBAC system.

---

# 19. So I would freeze these architecture decisions

### Decision 1 — Platform role

```text
User.role

CUSTOMER
PROVIDER
ADMIN
```

### Decision 2 — Provider organization role

```text
ProviderMembership.role

OWNER
MANAGER
AGENT
```

### Decision 3 — Agent type

```text
AgentType

MOBILE
ON_SITE
HYBRID
```

### Decision 4 — Organization

```text
One organization
       ↓
Multiple provider locations/branches
```

### Decision 5 — Customer addresses

```text
User
 ↓
UserAddress
 ↓
Address
```

### Decision 6 — Provider addresses

```text
ProviderOrganization
 ↓
ProviderLocation
 ↓
Address
```

### Decision 7 — Booking address

```text
UserAddress / ProviderLocation
             ↓
       BookingLocation
             ↓
     Historical snapshot
```

### Decision 8 — Adding members

Use:

```text
Invitation
```

not:

```text
Owner creates Gmail/password
```

### Decision 9 — Provider creation

Support both:

```text
Existing customer → Become Provider
```

and:

```text
Direct Provider Registration
```

but both end in the same:

```text
User
+
ProviderOrganization
+
OWNER ProviderMembership
```

---

## This changes our V1 build order

I agree with you that **we should not continue building models yet**.

We should first lock:

```text
1. Identity architecture
       ↓
2. Organization architecture
       ↓
3. Address architecture
       ↓
4. Membership/invitation architecture
       ↓
5. Agent architecture
       ↓
6. Registration/login flows
       ↓
7. Permission rules
       ↓
8. Database tables
       ↓
9. SQLAlchemy models
       ↓
10. Alembic migration
       ↓
11. APIs
       ↓
12. Frontend flows
```

The biggest architectural change from our earlier design is that **`User` will now have a platform role again**, while `ProviderMembership` remains responsible for the organization-specific role. That gives you the simpler model you were looking for without losing the organization-level access control.

Lock the remaining architecture choice

* Define the exact role and permission matrix
