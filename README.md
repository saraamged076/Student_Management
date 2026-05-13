# Student Management System

A backend REST API project built using FastAPI for managing students with authentication, authorization, Redis caching, logging, monitoring, and testing.

---

# Features

* User Registration & Login
* JWT Authentication
* Refresh Tokens
* Role-Based Authorization (Admin / Student)
* CRUD Operations for Students
* Ownership Authorization
* Redis Caching
* Cache-Aside Pattern
* Cache Invalidation
* Logging System
* Monitoring Dashboard
* Response Time Monitoring
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
* HTML
* CSS
* JavaScript

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
├── monitoring.py
└── main.py

templates/
└── dashboard.html
```

---

# Installation

## 1) Clone the repository

```bash
git clone https://github.com/saraamged076/Student_Management
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

# Monitoring Dashboard

Dashboard URL:

```text
http://127.0.0.1:8000/dashboard
```

The dashboard displays:

* Total API Requests
* Cache Hits
* Error Count
* Response Time
* System Health Status

Metrics Endpoint:

```http
GET /metrics
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
GET /students/{id}
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
redis_client.delete(f"student:{student_id}")
```

---

# Logging System

The application uses Python logging to track:

* CRUD operations
* Errors and exceptions
* Authentication events
* Request monitoring

Log levels used:

* INFO
* WARNING
* ERROR

Logs are stored inside:

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

The test suite covers:

* Authentication tests
* Authorization tests
* CRUD operations
* Edge cases
* Error handling
* Invalid login attempts
* Duplicate users
* Missing resources

---

# Main Endpoints

## Authentication

```http
POST /auth/register
POST /auth/login
POST /auth/refresh
GET /auth/me
GET /auth/admin-only
```

---

## Students

```http
GET /students
GET /students/{id}
POST /students
PUT /students/{id}
DELETE /students/{id}
```

---

# Monitoring Features

The system tracks:

* Total Requests
* Cache Hits
* Error Counts
* API Response Time
* System Health Status

---

# Author

Developed as a backend learning project using FastAPI and modern backend development concepts.
