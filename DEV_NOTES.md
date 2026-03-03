# DotCampus Discussion API — Learning Notes

This file documents the architectural and conceptual learning behind building a secure RESTful API using Django REST Framework and JWT authentication.

---

# 1. Why We Created a Custom User Model First

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

# 2. What is Django REST Framework (DRF)?

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

# 3. What is a Serializer?

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

# 4. Why Not Save Password Directly?

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

# 5. What is JWT?

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

# 6. What is Authentication vs Authorization?

## Authentication:

> Who are you?

## Authorization:

> Are you allowed to do this?

## Example:

- JWT verifies identity (authentication).
- Role field determines permission (authorization).

---

# 7. Why We Created users/urls.py and discussions/urls.py

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

# 8. Why We Commit Frequently

**Frequent commits:**

- Protect work
- Show incremental thinking
- Allow rollback
- Improve clarity
- Demonstrate professional workflow

---
