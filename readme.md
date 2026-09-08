# HRM System

A Human Resource Management System backend built with **FastAPI** and **PostgreSQL**.

The system provides APIs for managing users, employees, departments, designations, roles, permissions, salaries, projects, leaves, and attendance. It also includes JWT authentication, password security, role-based authorization, and permission-based authorization.

## Technologies

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Psycopg
* JWT
* pwdlib / Argon2
* Uvicorn

## Features

* User & Employee Management
* Departments & Designations
* Roles & Permissions
* Salaries
* Projects & Employee Projects
* Leaves & Attendance
* JWT Authentication
* Password Hashing
* Password Reset
* Role-Based Authorization
* Permission-Based Authorization

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/alishakeel15/HRM_System.git
cd HRM_System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure `.env`

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/hrm_system_db

SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
RESET_TOKEN_EXPIRE_MINUTES=15
```

**Do not upload `.env` to GitHub.**

## Database

Create a PostgreSQL database:

```text
hrm_system_db
```

Make sure PostgreSQL is running.

## Run

```bash
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Authentication

The system uses JWT Bearer Authentication.

Main authentication endpoints:

```text
POST   /auth/signup
POST   /auth/login
GET    /auth/me
PATCH  /auth/change-password
POST   /auth/forgot-password
POST   /auth/reset-password
POST   /auth/logout
```

## Security

* Passwords are hashed using Argon2.
* JWT tokens have expiration times.
* Protected routes use role and permission checks.
* Sensitive configuration is stored in `.env`.

## License

This project is developed for HRM backend development and learning purposes.
