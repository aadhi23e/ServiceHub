Yes. For a **real production application**, I think your separation is better than making `ProviderMembership` the only way to determine whether an account is a provider.

The important part is to define exactly what each layer means.

## 1. Final identity design

I would use **three levels**:

```text
User
│
├── role = CUSTOMER
│
├── role = PROVIDER
│      │
│      └── ProviderProfile
│             │
│             └── ProviderOrganization(s)
│                    │
│                    └── ProviderMembership
│                           ├── OWNER
│                           ├── MANAGER
│                           └── AGENT
│
└── role = ADMIN
```

However, there is one thing I would change from your wording:

> `users.role = PROVIDER` → search "provider table"

Yes, but the **provider table should represent the user's provider identity**, while the organization/member tables represent the business relationship.

So:

```text
users
------
id
email
password_hash
role
status
...
```

```text
provider_profiles
-----------------
id
user_id        → users.id
...
```

```text
provider_organizations
----------------------
id
name
...
```

```text
provider_memberships
--------------------
id
user_id              → users.id
organization_id      → provider_organizations.id
role                 → OWNER / MANAGER / AGENT
agent_type           → MOBILE / ON_SITE / HYBRID / NULL
...
```

This gives us a very clear separation.

---

# 2. Why I like this for ServiceHub

Suppose:

```text
User
id = 101
role = PROVIDER
```

Backend can immediately know:

> This account is a provider account.

Then:

```text
provider_profiles
user_id = 101
```

tells us the provider-specific profile.

Then:

```text
provider_memberships
user_id = 101
organization_id = XYZ
role = OWNER
```

tells us:

> This provider is the owner of organization XYZ.

This is much cleaner than trying to put:

```text
OWNER
MANAGER
AGENT
CUSTOMER
ADMIN
PROVIDER
```

all into one `users.role`.

---

# 3. But don't use `users.role` alone for authorization

This is extremely important for security.

For example:

```text
User
role = PROVIDER
```

does **not** automatically mean:

> "This user can modify every provider organization."

The backend must still check:

```text
User
 ↓
ProviderMembership
 ↓
Organization
 ↓
Membership role
 ↓
Permission
```

For example:

```text
POST /organizations/{organization_id}/services
```

Backend checks:

```text
1. Is authenticated?
2. Is user ACTIVE?
3. Is user a PROVIDER?
4. Does membership exist for this organization?
5. Is membership ACTIVE?
6. Is membership role allowed to create services?
7. Is organization ACTIVE?
8. Is the requested operation valid?
```

This is how we make the application robust rather than simply hiding buttons in the frontend.

---

# 4. Platform roles

For V1, I recommend:

| Role       | Meaning                                                        |
| ---------- | -------------------------------------------------------------- |
| `CUSTOMER` | Can use ServiceHub as a customer                               |
| `PROVIDER` | Has a provider account and can operate a provider organization |
| `ADMIN`    | Platform-level ServiceHub administrator                        |

So:

```text
User.role
────────────
CUSTOMER
PROVIDER
ADMIN
```

### Important

A `PROVIDER` can still behave as a customer.

For example:

```text
User
role = PROVIDER

Provider organization
    OWNER

AND

Customer bookings
    Booking #123
    Booking #456
```

We shouldn't force someone to maintain two accounts just because they own a business.

---

# 5. Provider organization roles

Then separately:

```text
ProviderMembership.role
───────────────────────
OWNER
MANAGER
AGENT
```

And:

```text
ProviderMembership.agent_type
─────────────────────────────
NULL        → OWNER / MANAGER
MOBILE      → AGENT
ON_SITE     → AGENT
HYBRID      → AGENT
```

We should enforce that `agent_type` is only populated for `AGENT`.

---

# 6. Now the exact permission matrix

I would **not** make a giant enterprise RBAC system for V1.

We can have explicit backend permission rules based on:

```text
platform role
+
organization membership role
+
resource ownership
+
resource state
```

Here is the V1 matrix.

## Platform-level permissions

| Capability                      | Customer |      Provider      |      Admin     |
| ------------------------------- | :------: | :----------------: | :------------: |
| Register/login                  |     ✅    |          ✅         |        ✅       |
| Manage own account              |     ✅    |          ✅         |        ✅       |
| Manage own addresses            |     ✅    |          ✅         |        ✅       |
| Browse services                 |     ✅    |          ✅         |        ✅       |
| Create customer booking         |     ✅    |          ✅         |       ✅*       |
| View own bookings               |     ✅    |          ✅         |       ✅*       |
| Manage provider organization    |     ❌    | Through membership | Platform-level |
| Verify providers                |     ❌    |          ❌         |        ✅       |
| Manage platform users           |     ❌    |          ❌         |        ✅       |
| Manage provider verification    |     ❌    |          ❌         |        ✅       |
| View platform audit information |     ❌    |          ❌         |        ✅       |

`*` Admin access should be controlled separately and carefully; we don't want admins behaving as ordinary customers by accident.

---

# 7. Provider organization permission matrix

This is the important one.

| Capability                   | OWNER | MANAGER |       AGENT       |
| ---------------------------- | :---: | :-----: | :---------------: |
| View organization            |   ✅   |    ✅    |      Limited      |
| Edit organization profile    |   ✅   | Limited |         ❌         |
| Manage organization settings |   ✅   | Limited |         ❌         |
| Add branch/location          |   ✅   |    ✅    |         ❌         |
| Edit branch/location         |   ✅   |    ✅    |         ❌         |
| Delete/deactivate branch     |   ✅   | Limited |         ❌         |
| Create service               |   ✅   |    ✅    |         ❌         |
| Edit service                 |   ✅   |    ✅    |         ❌         |
| Activate/deactivate service  |   ✅   |    ✅    |         ❌         |
| Archive service              |   ✅   | Limited |         ❌         |
| Create service requirements  |   ✅   |    ✅    |         ❌         |
| Manage service areas         |   ✅   |    ✅    |         ❌         |
| Manage operating hours       |   ✅   |    ✅    |         ❌         |
| View agents                  |   ✅   |    ✅    | Own/assigned data |
| Invite member                |   ✅   |    ✅    |         ❌         |
| Change member role           |   ✅   | Limited |         ❌         |
| Suspend member               |   ✅   | Limited |         ❌         |
| Remove member                |   ✅   | Limited |         ❌         |
| Manage OWNER                 |   ❌*  |    ❌    |         ❌         |
| Transfer ownership           |   ✅   |    ❌    |         ❌         |
| Delete organization          |  ✅**  |    ❌    |         ❌         |

`*` An owner shouldn't be casually modified by another owner in V1.

`**` We should probably implement **deactivation**, not physical deletion, for an organization with historical data.

---

# 8. Booking permissions

This needs more detail because booking ownership matters.

| Action                            |  OWNER  |   MANAGER   |       AGENT      |
| --------------------------------- | :-----: | :---------: | :--------------: |
| View organization bookings        |    ✅    |      ✅      |   Assigned only  |
| Create booking for customer       |    ✅    |      ✅      |         ❌        |
| Confirm booking                   |    ✅    |      ✅      |         ❌        |
| Reschedule booking                |    ✅    |      ✅      |      Limited     |
| Cancel booking                    |    ✅    |      ✅      |    Limited/No    |
| Assign agent                      |    ✅    |      ✅      |         ❌        |
| Reassign agent                    |    ✅    |      ✅      |         ❌        |
| Accept assignment                 |    ❌    |      ❌      |         ✅        |
| Decline assignment                |    ❌    |      ❌      |         ✅        |
| Mark en route                     |    ❌    |      ❌      |         ✅        |
| Mark arrived                      |    ❌    |      ❌      |         ✅        |
| Start service                     |    ❌    |   Limited   |         ✅        |
| Complete service                  |    ❌    |   Limited   |         ✅        |
| View customer service information |  Broad  | Operational | Assigned booking |
| Modify payment                    | Limited |   Limited   |         ❌        |
| Issue refund                      |    ✅    |  Controlled |         ❌        |

The agent should **not** automatically see everything about the customer.

The API should return only information required to perform the assigned service.

That's an important security principle.

---

# 9. Agent-specific permissions

The agent's capabilities should depend on both:

```text
membership.role == AGENT
```

and:

```text
agent_type
```

For example:

```text
AGENT
agent_type = MOBILE
```

can be assigned:

```text
HOME_SERVICE
```

while:

```text
AGENT
agent_type = ON_SITE
```

can primarily work:

```text
AT_PROVIDER
```

But we shouldn't rely on `agent_type` alone.

The final assignment check should be something like:

```text
Agent
   ↓
Active membership?
   ↓
Correct organization?
   ↓
Correct agent capability?
   ↓
Service supports this mode?
   ↓
Agent available?
   ↓
No time-off conflict?
   ↓
No assignment overlap?
   ↓
Travel/schedule feasible?
   ↓
Assignment allowed
```

That is much safer.

---

# 10. Ownership rules

We also need **resource ownership checks**, not just roles.

For example, suppose:

```text
Organization A
Organization B

Manager A
```

Manager A sends:

```http
DELETE /api/v1/services/service-from-organization-B
```

Even though Manager A is a valid manager, the request must be rejected.

The backend must check:

```text
service.organization_id == current_user.organization_id
```

or equivalent membership lookup.

So authorization becomes:

```text
Authentication
       ↓
Platform role
       ↓
Organization membership
       ↓
Membership role
       ↓
Resource belongs to organization
       ↓
Resource state allows operation
       ↓
Permission
```

This is the model I want us to implement.

---

# 11. Admin is different

Admin should **not** be an organization membership role.

An admin is a ServiceHub platform operator.

For V1:

```text
users.is_admin = true
```

or:

```text
users.role = ADMIN
```

We need to choose one.

Since you now want:

```text
users.role
```

I recommend:

```text
UserRole
────────────
CUSTOMER
PROVIDER
ADMIN
```

and **remove `is_admin`**.

It's cleaner because we don't have:

```text
role = CUSTOMER
is_admin = true
```

which creates two sources of truth.

---

# 12. What about a provider OWNER who is also an admin?

Don't support that as an ordinary business flow in V1.

Platform admin is a privileged ServiceHub account.

If an actual employee of ServiceHub also happens to have a provider account, that can be handled explicitly later, but we shouldn't design our authorization around mixing platform administration with provider business roles.

---

# 13. Provider creation flow

With this model:

### Existing customer

```text
USER
role = CUSTOMER
     │
     │ "Become a Provider"
     ▼
Provider Profile
     │
     ▼
Provider Organization
status = PENDING
     │
     ▼
Provider Membership
role = OWNER
     │
     ▼
Admin verification
     │
     ▼
Organization ACTIVE
```

Then:

```text
USER.role
CUSTOMER → PROVIDER
```

---

### Direct provider registration

```text
Register as Provider
        ↓
USER
role = PROVIDER
        ↓
Provider Profile
        ↓
Provider Organization
        ↓
OWNER membership
        ↓
Verification
        ↓
ACTIVE
```

Both flows end in the same structure.

---

# 14. Adding employees

This is where our invitation architecture comes in.

### Owner adds manager

```text
OWNER
  ↓
Enter email
  ↓
Select MANAGER
  ↓
Invitation
  ↓
Existing user?
   ├── YES → connect membership
   │
   └── NO  → create account through invitation
  ↓
ProviderMembership
role = MANAGER
```

### Owner/Manager adds agent

```text
OWNER / MANAGER
       ↓
Enter email
       ↓
Role = AGENT
       ↓
Agent Type
       ↓
MOBILE / ON_SITE / HYBRID
       ↓
Invitation
       ↓
Provider Membership
```

Again, **we should never have the owner create a Gmail account or know the employee's password.**

---

# 15. Address model

I would now slightly refine our previous address decision.

Don't make one generic address table with ambiguous ownership.

Use:

```text
users
   │
   └── user_addresses

provider_organizations
   │
   └── provider_locations
          │
          └── address information
```

And:

```text
bookings
   │
   └── booking_locations
```

So the meanings are crystal clear:

```text
UserAddress
= customer's saved address

ProviderLocation
= organization's branch/shop/service center

BookingLocation
= location used for THIS booking
```

This is safer for historical records.

---

# 16. The architecture I would freeze

For **ServiceHub V1.0.0**, I would now freeze the identity model as:

```text
┌─────────────────────────────────────┐
│               USER                  │
├─────────────────────────────────────┤
│ id                                  │
│ email                               │
│ password_hash                       │
│ role                                │
│ status                              │
│ ...                                 │
└──────────────────┬──────────────────┘
                   │
        ┌──────────┼───────────┐
        │          │           │
     CUSTOMER   PROVIDER     ADMIN
                   │
                   ▼
          ┌─────────────────┐
          │ ProviderProfile │
          └────────┬────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │ ProviderOrganization   │
       └────────────┬───────────┘
                    │
                    ├── Locations
                    ├── Services
                    ├── Service Areas
                    ├── Operating Hours
                    │
                    └── Memberships
                           │
                ┌──────────┼──────────┐
                │          │          │
              OWNER     MANAGER     AGENT
                                      │
                                      ▼
                                 AgentType
```

And the security model:

```text
REQUEST
   ↓
Authentication
   ↓
User ACTIVE?
   ↓
Platform role?
   ↓
Organization membership?
   ↓
Membership ACTIVE?
   ↓
Membership role?
   ↓
Resource belongs to organization?
   ↓
Resource state valid?
   ↓
Permission allowed?
   ↓
Perform operation
   ↓
Audit/log important action
```

That is the foundation I would use for a **real-user production application**.

### One final recommendation

I would **not start writing the new SQLAlchemy models yet**.

We should first turn this into an explicit V1 **Authorization & Identity Architecture document**, including:

1. `UserRole`
2. `ProviderMembershipRole`
3. `AgentType`
4. registration flows
5. provider creation flow
6. invitation flow
7. organization lifecycle
8. exact permissions
9. ownership rules
10. authentication vs authorization rules
11. security/error behavior
12. address ownership
13. what happens when accounts are suspended/deactivated
14. what happens when a manager/agent is removed
15. audit requirements

Once that is frozen, **then** we update the database schema and models. That prevents us from having to redesign the database again halfway through V1.
