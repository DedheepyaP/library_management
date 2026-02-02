-Library Management System-

FastAPI-based backend service for managing a digital library.
It supports book management, users, borrowing & returning books, and maintains transactional integrity using a relational database.

-Features-

- Book management (add, list, track availability)
- User management
- Borrow and return books with transaction safety
- Loan tracking with status (borrowed / returned)
- PostgreSQL database with SQLAlchemy ORM
- Database migrations using Alembic
- Dockerized for local development & deployment

-Tech Stack-

- FastAPI – API framework
- SQLAlchemy – ORM
- PostgreSQL – Database
- Alembic – Schema migrations
- Poetry – Dependency management
- Docker & Docker Compose – Containerization

-Environment Variables-

Create a .env file in the project root:
DATABASE_URL=postgresql+psycopg2://librodb:libropass@db:5432/libro

-Run with Docker-

Build & start services:
>> docker compose up --build

API will be available at
http://localhost:8000

-Swagger Docs-
http://localhost:8000/docs

-Database Migrations (Alembic)-

Create a new migration after modifying SQLAlchemy models in app/db/models.py:
>> alembic revision --autogenerate -m "your message"

Apply migrations
>> alembic upgrade head
