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
