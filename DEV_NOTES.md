# DotCampus Discussion API — LEARNING NOTES

This file documents the architectural and conceptual learning behind building a secure RESTful API using Django REST Framework and JWT authentication.

---

# 1. WHY WE CREATED A CUSTOM User MODEL FIRST

## Problem:

Django has a default User model (`auth_user`).

## Risk:

If you run migrations before creating your own custom user model:

- Django creates the default user table.
- Other tables may link to it.
- Changing user model later becomes extremely complex.

## Solution:

We created a custom user model BEFORE first migration.

```python
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        MENTOR = "mentor", "Mentor"
        LEARNER = "learner", "Learner"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.LEARNER)
```

**Why extend AbstractUser?**

- Keeps username, password, email logic.
- Lets us add custom fields (like role).
- Avoids rebuilding authentication system.

---

# 2. WHAT IS DJANGO REST FRAMEWORK (DRF)?

Django by default returns HTML.

DRF transforms Django into an API framework:

- Accepts JSON
- Returns JSON
- Handles API authentication
- Provides serializers
- Provides API views
- Provides permission system
  Without DRF, building APIs would require much more manual work.

---

# 3. WHAT IS A SERIALIZER?

## A serializer is:

> A translator between JSON and Django models.

## It does 3 things:

- Validates incoming JSON
- Converts JSON → Python objects
- Converts Python objects → JSON responses

## Example:

**Incoming JSON:**

```json
{
  "username": "ibrahim",
  "password": "StrongPass123"
}
```

**Serializer checks:**

- Is username provided?
- Is password long enough?
- If valid → creates user safely.

---

# 4. WHY NOT SAVE PASSWORD DIRECTLY?

**We used:**

```python
User.objects.create_user(...)
```

**Instead of:**

```python
User.objects.create(...)
```

**Why?**

**Because `create_user()`:**

- Hashes password securely
- Follows Django authentication rules

If we used .create(), password would be stored as plain text.

---

# 5. WHAT IS JWT?

JWT = JSON Web Token

Instead of sessions (cookies), APIs use tokens.

## Login flow:

1. User sends username + password.
2. Server returns:
   - access token
   - refresh token

**Every protected request must include:**

```code
Authorization: Bearer <access_token>
```

**Server verifies:**

- Is token valid?
- Is token expired?
- Which user does this token belong to?

No server-side session storage required.

Stateless authentication.

---

# 6. WHAT IS AUTHENTICATION VS. AUTHORIZATION?

## Authentication:

> Who are you?

## Authorization:

> Are you allowed to do this?

## Example:

- JWT verifies identity (authentication).
- Role field determines permission (authorization).

---

# 7. WHY WE CREATED users/urls.py AND discussions/urls.py

Django requires included URL modules to exist.

**In config/urls.py we wrote:**

```python
path("api/", include("discussions.urls"))
```

If `discussions/urls.py` doesn't exist:
Django crashes with:

ModuleNotFoundError

## Lesson:

Always create URL modules before including them.

---

# 8. WHY WE COMMIT FREQUENTLY

**Frequent commits:**

- Protect work
- Show incremental thinking
- Allow rollback
- Improve clarity
- Demonstrate professional workflow

---

# 9. DESIGNING THE DISCUSSION MODELS

**What is a Discussion?**

A discussion must have:

- title
- body/content
- author (User)
- created_at
- updated_at

## Relationship Design

**Who owns it?**

A discussion belongs to exactly one user.

This creates a:

User (1) → Discussion (many) relationship.

We implemented:

```python
author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="discussions"
)
```

## Why settings.AUTH_USER_MODEL?

Instead of importing User directly, we use:

```python
settings.AUTH_USER_MODEL
```

This keeps the model flexible and compatible with our custom user model.

## Why related_name="discussions"?

It allows:

```python
user.discussions.all()
```

Instead of Django's default:

```python
user.discussion_set.all()
```

Cleaner naming improves readability.

## Why auto_now_add vs auto_now?

- auto_now_add=True → set only when created.
- auto_now=True → updates every time the object is saved.

This ensures proper tracking of creation and modification timestamps.

## Architectural Principle

Models define the shape of your database.

Everything else (serializers, views, permissions) depends on models.

So model design must be intentional and clear before building

---

# 10. IMPLEMENTING DISCUSSION CRUD WITH ModelViewSet

## What is a ModelSerializer?

ModelSerializer automatically maps model fields to JSON fields and handles validation and saving.

It reduces boilerplate code and keeps API logic clean.

## Why is author ReadOnly?

We defined:

```python
author = serializers.ReadOnlyField(source="author.username")
```

This ensures:

- Users cannot manually assign an author.
- Ownership is determined by the authenticated user.
- Prevents impersonation.

## What is a ModelViewSet?

ModelViewSet automatically provides full CRUD functionality:

- list → GET /discussions/
- retrieve → GET /discussions/{id}/
- create → POST
- update → PUT
- partial_update → PATCH
- destroy → DELETE

Instead of writing multiple views, everything is handled in one class.

## What is `perform_create()`?

When creating a discussion, we override:

```python
def perform_create(self, serializer):
    serializer.save(author=self.request.user)
```

This automatically assigns the currently authenticated user as the author.

It enforces ownership securely.

## What is a Router?

A DefaultRouter automatically generates RESTful URLs for ViewSets.

Instead of manually writing URL patterns, the router generates:

- GET /api/discussions/
- POST /api/discussions/
- GET /api/discussions/{id}/
- PUT /api/discussions/{id}/
- DELETE /api/discussions/{id}/

This keeps the API clean and scalable.

## Architectural Insight

Model → Serializer → ViewSet → Router

Each layer builds on the previous one.

Models define data.
Serializers validate and transform data.
ViewSets define behavior.
Routers expose endpoints.

---

# 11. UNDERSTANDING JWT AUTHENTICATION IN PRACTICE

## Why POST Failed Without Token

Our DiscussionViewSet uses:

permission_classes = [IsAuthenticatedOrReadOnly]

This means:

- GET requests are allowed for everyone.
- POST, PUT, DELETE require authentication.

Without authentication, the API returns 401 Unauthorized.

---

## What Happens During Login?

We use the endpoint:

POST /api/auth/login/

When valid credentials are provided, the server returns:

{
"refresh": "...",
"access": "..."
}

---

## What Is Access vs Refresh Token?

Access Token:

- Short-lived
- Used to access protected endpoints

Refresh Token:

- Long-lived
- Used to request new access tokens

For most API calls, we use the ACCESS token.

---

## How To Use JWT In Postman

1. Login to obtain access token.
2. Copy the access token.
3. In Postman:
   - Go to Authorization tab
   - Select "Bearer Token"
   - Paste the access token
4. Send the request.

Postman automatically sends:

Authorization: Bearer <access_token>

---

## What Happens Internally?

When the request reaches the server:

1. JWTAuthentication reads the Authorization header.
2. Validates the token.
3. Decodes the payload.
4. Extracts user_id.
5. Sets request.user.

This is why:

serializer.save(author=self.request.user)

works correctly.

Without token:
request.user = AnonymousUser

With token:
request.user = Logged-in user

---

# 12. IMPLEMENTING ROLE-BASED OBJECT PERMISSIONS

## Why Default Permissions Were Not Enough

Using IsAuthenticatedOrReadOnly only checks:

- Is user logged in?

It does NOT check:

- Who owns the object?
- What role the user has?

So we created a custom permission class.

---

## What is Object-Level Permission?

Object-level permissions run when accessing a specific object.

They allow fine-grained control like:

- "User can only edit their own discussion"
- "Mentor can edit any discussion"
- "Admin has full access"

---

## Custom Permission Logic

We created:

class IsAuthorOrRoleBased(BasePermission)

Inside:

def has_object_permission(self, request, view, obj):

### Logic Flow:

1. SAFE_METHODS (GET, HEAD, OPTIONS) → allowed for everyone.
2. If role is admin → full access.
3. If role is mentor → allow update only.
4. Otherwise → only author can modify.

---

## Why Order Matters

Permissions are evaluated top-down.

We check:

- Admin first
- Then mentor
- Then ownership

This creates a clear hierarchy.

---

## Key Concept

Authentication answers:
"Who are you?"

Authorization answers:
"What are you allowed to do?"

We are now implementing real authorization logic.
