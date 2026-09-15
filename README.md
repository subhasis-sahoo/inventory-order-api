# Inventory & Order Management API

A backend REST API built with **Python and FastAPI** for managing products, users, and orders.

This project was built as a hands-on backend learning project to practice building a production-style API using **FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, and pytest**.

## Features

### Product Management

* Create a product
* Get all products
* Get a product by ID
* Filter products by name and price range
* Update a product
* Partially update a product
* Delete a product

### User Management

* Create a user
* Get all users
* Get a user by ID
* Prevent duplicate email registration
* Get orders belonging to a user

### Order Management

* Create an order for a user
* Add multiple products to an order
* Validate user and product existence
* Validate available stock
* Automatically calculate order total
* Automatically reduce product stock
* Maintain order and order-item relationships
* Roll back the transaction if an error occurs

### Validation & Error Handling

* Request validation using Pydantic
* Custom business exceptions
* Proper HTTP status codes
* Duplicate email handling
* Product and user not-found handling
* Insufficient stock handling

### Database & Migrations

* PostgreSQL database
* SQLAlchemy ORM
* Foreign-key relationships
* Alembic database migrations
* Separate test database
* Environment-based database configuration

### Testing

* pytest
* FastAPI TestClient
* API integration tests
* Database tests
* Validation tests
* Transaction rollback tests
* Test database isolation

---

## Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Backend programming             |
| FastAPI       | REST API framework              |
| Pydantic      | Request/response validation     |
| SQLAlchemy    | ORM and database interaction    |
| PostgreSQL    | Relational database             |
| Alembic       | Database migrations             |
| pytest        | Testing                         |
| python-dotenv | Environment variable management |

---

## Project Architecture

The application follows a layered architecture:

```text
Client
   ↓
Router
   ↓
Service
   ↓
Repository
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

### Layer Responsibilities

**Router**

* Defines API endpoints
* Handles HTTP requests and responses
* Converts business exceptions into HTTP exceptions

**Service**

* Contains business logic
* Performs validations
* Coordinates repositories
* Handles business-level transactions

**Repository**

* Handles database operations
* Uses SQLAlchemy to interact with PostgreSQL

**Schemas**

* Defines request and response models
* Handles API data validation using Pydantic

**Database**

* Contains SQLAlchemy models
* Provides database connection and session management

---

## Project Structure

```text
inventory-order-api/
│
├── app/
│   ├── database/
│   │   ├── connection.py
│   │   ├── dependencies.py
│   │   └── models.py
│   │
│   ├── exceptions/
│   │
│   ├── repositories/
│   │
│   ├── routers/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── conftest.py
│   └── ...
│
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Database Relationships

The application uses the following relationships:

```text
User
 │
 │ 1
 │
 │ *
 ▼
Order
 │
 │ 1
 │
 │ *
 ▼
OrderItem
 │
 │ *
 │
 │ 1
 ▼
Product
```

A user can have multiple orders.

An order can contain multiple order items.

Each order item refers to a product.

---

## Environment Configuration

Database credentials are stored in a local `.env` file and are **not committed to GitHub**.

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/inventory_db

TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/inventory_test_db
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

> Never commit your `.env` file or database credentials to GitHub.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Subhasis-Sahoo/inventory-order-api.git
cd inventory-order-api
```

Create a virtual environment:

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Database Setup

Create the required PostgreSQL databases:

```text
inventory_db
inventory_test_db
```

Configure the database URLs in `.env`.

Run the latest Alembic migrations:

```powershell
alembic upgrade head
```

Check the current migration:

```powershell
alembic current
```

---

## Run the Application

Start the FastAPI development server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Running Tests

Run the complete test suite:

```powershell
python -m pytest
```

The project uses a separate PostgreSQL database for testing to keep test data isolated from the development database.

---

## Database Migrations

Create a new migration after changing SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "describe your change"
```

Apply migrations:

```powershell
alembic upgrade head
```

Rollback the latest migration:

```powershell
alembic downgrade -1
```

View migration history:

```powershell
alembic history
```

---

## Example API Endpoints

### Products

```text
POST   /products/
GET    /products/
GET    /products/{product_id}
PUT    /products/{product_id}
PATCH  /products/{product_id}
DELETE /products/{product_id}
```

### Users

```text
POST   /users/
GET    /users/
GET    /users/{user_id}
GET    /users/{user_id}/orders
```

### Orders

```text
POST   /orders/
```

---

## What I Practiced Through This Project

This project was primarily built to gain practical experience with backend development concepts, including:

* REST API development
* FastAPI routing
* Dependency injection
* Pydantic validation
* SQLAlchemy ORM
* PostgreSQL
* Foreign keys and relationships
* Service-repository architecture
* Business logic separation
* Database transactions
* Rollback handling
* Custom exceptions
* HTTP error handling
* Alembic migrations
* Environment variables
* Automated API testing
* Test database isolation
* Git and GitHub workflow

---

## Future Improvements

Potential future improvements include:

* JWT-based authentication
* Role-based authorization
* Password hashing
* Pagination
* Async database operations
* Redis caching
* Background tasks
* Docker containerization
* CI/CD pipeline
* API deployment

---

## Author

**Subhasis Sahoo**

Software Engineer | Python Backend Developer

GitHub: [Subhasis-Sahoo](https://github.com/Subhasis-Sahoo)
