# DotCampus Discussion API (DRF) 💬🔐

A secure RESTful discussion platform API for the DotCampus Learning Community built with **Django REST Framework**.

It supports:

- JWT authentication
- Role-based authorization (admin, mentor, learner)
- Discussion threads
- Nested comments
- Automated testing (95% coverage)

---

## 🚀 Live URL

- **Base API:** https://dotcampus-discussion-drf.onrender.com/api/discussions/

> ⚠️ Note: Free-tier instances may sleep after inactivity.

---

## 📚 API Documentation (Swagger)

- **Docs:** https://dotcampus-discussion-drf.onrender.com/api/docs/

> Render free tier may sleep, first load can take a bit.”

---

## ✅ Features

### Authentication

- User registration (sign up)
- User login using JWT (access + refresh tokens)

### Roles & Permissions

- **Learner**
  - View all discussions
  - View a single discussion
  - Create a discussion
  - Update **own** discussion
  - Delete **own** discussion
  - View comments on a discussion
  - Comment on a discussion

- **Mentor**
  - Everything a learner can do
  - Update **any** discussion

- **Admin**
  - Everything a mentor can do
  - Delete **any** discussion
  - Delete **any** comment
  - (Optional/Admin Panel) Manage users and roles

### Discussions & Comments

- Full CRUD for discussions with ownership + role rules
- Commenting system with nested endpoint:
  - `GET /api/discussions/<id>/comments/`
  - `POST /api/discussions/<id>/comments/`

### Testing

- Automated API tests
- Permission validation tests
- Role enforcement tests
- Ownership validation tests
- **95% code coverage**

---

## 🛠️ Tech Stack

- Django 5
- Django REST Framework
- JWT (SimpleJWT)
- PostgreSQL (production)
- SQLite (local)
- API Docs: drf-spectacular (Swagger)
- Deployment: Render
- Static files: WhiteNoise
- Server: Gunicorn

---

## ⚙️ Local Setup

### 1. Clone repo

```bash
git clone https://github.com/iibrahimx/dotcampus-discussion-drf.git
cd dotcampus-discussion-drf
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Start server

```bash
python manage.py runserver
```

API runs at:

- http://127.0.0.1:8000

Swagger docs:

- http://127.0.0.1:8000/api/docs/

## 🔐 Environment Variables (Production)

Set these on Render:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgres://...
```

## 🧪 Run Tests + Coverage

```bash
python manage.py test
```

Coverage:

```bash
coverage run manage.py test
coverage report -m
```

## 👤 Author

Ibrahim Ibrahim
GitHub: https://github.com/iibrahimx
