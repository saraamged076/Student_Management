# Student Management System

A backend REST API project built using FastAPI for managing students with authentication, authorization, Redis caching, logging, and testing.

---

# Features

* User Registration & Login
* JWT Authentication
* Refresh Tokens
* Role-Based Authorization (Admin / Student)
* CRUD Operations for Students
* Ownership Authorization
* Redis Caching
* Cache Invalidation
* Logging System
* API Testing with Pytest
* Swagger API Documentation

---

# Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Redis
* Pytest

---

# Project Structure

```bash
app/
│
├── models/
├── schemas/
├── services/
├── routers/
├── test/
├── auth.py
├── database.py
├── redis_client.py
├── logging_config.py
└── main.py
```

---

# Installation

## 1) Clone the repository

```bash
git clone <https://github.com/saraamged076/Student_Management>
cd student_management
```

---

## 2) Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

---

## 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Start Redis Server

```bash
redis-server.exe
```

---

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Authentication System

The project uses JWT Authentication.

## Access Token

Used to access protected routes.

## Refresh Token

Used to generate a new access token without logging in again.

---

# Role-Based Authorization

## Admin

Can:

* Delete students
* Update any student

## Student

Can:

* Create students
* Update only their own students

---

# Redis Caching

The project uses Redis to cache:

```http
GET /students
```

## Cache Strategy

Cache-Aside Pattern:

1. Check Redis cache
2. If data exists → return cached data
3. If data does not exist → fetch from database
4. Store data in Redis

---

# Cache Invalidation

When:

* Creating student
* Updating student
* Deleting student

The cache is cleared using:

```python
redis_client.delete("students")
```

---

# Logging System

The project logs important operations into:

```text
app.log
```

Examples:

```text
INFO - Student created
INFO - Student updated
WARNING - Student deleted
```

---

# Testing

The project uses Pytest for API testing.

Run tests:

```bash
python -m pytest
```

---

# Main Endpoints

## Authentication

```http
POST /auth/register
POST /auth/login
POST /auth/refresh
GET /auth/me
```

---

## Students

```http
GET /students
POST /students
GET /students/{id}
PUT /students/{id}
DELETE /students/{id}
```

---

# Author

Developed as a backend learning project using FastAPI and modern backend development co
