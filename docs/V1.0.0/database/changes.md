## USER Table

### V0.0.1
users
├── role
│   ├── CUSTOMER
│   ├── PROVIDER
│   └── ADMIN
│
└── provider_profile

### V1.0.0
users
├── is_admin
│
├── provider_memberships
│      └── provider_organization
│             ├── OWNER
│             ├── MANAGER
│             └── AGENT
│
└── customer behavior

#### Example relation
So a user can now legitimately be:
```
User A
├── is_admin = false
├── customer
└── ProviderMembership
       ├── provider = ABC Services
       └── role = OWNER
```
And another user can be:
```
User B
├── customer
└── ProviderMembership
       ├── provider = ABC Services
       └── role = AGENT
```