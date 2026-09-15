# Financial Operations Copilot

An AI-powered backend for personal and business financial operations built with **FastAPI**, **PostgreSQL** (Async SQLAlchemy), **LangGraph**, and **OpenAI GPT-4o**.

---

## Features

- **Authentication & RBAC**: JWT-based user authentication (Access & Refresh tokens) with role-based access control (`user`, `admin`).
- **Expense Management**:
  - Full CRUD operations with category enforcement (`Food`, `Transportation`, `Housing`, `Utilities`, `Entertainment`, `Health`, `Shopping`, `Others`).
  - Keyword search across descriptions and categories.
  - Spending summaries and aggregations by category and custom date ranges.
- **AI Copilot Agent**:
  - ReAct agent powered by LangGraph and OpenAI.
  - Natural language parsing for recording expenses, querying transactions, and generating financial summaries.
  - Function calling tools integrated directly with the database services.

---

## Tech Stack

- **Framework**: FastAPI
- **Database & ORM**: PostgreSQL, SQLAlchemy 2.0 (Asyncpg), Pydantic v2
- **AI / Agent**: LangGraph, LangChain, OpenAI (`gpt-4o`)
- **Security**: JWT (joserfc), Passlib (Argon2/Bcrypt)

---

## Getting Started

### 1. Prerequisites

- Python 3.11+
- PostgreSQL database instance

### 2. Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

DB_NAME=fincopilot
DB_HOST=localhost
DB_PORT=5432
DB_USER=root
DB_PASS=your_db_password

ALG=HS256
SECRET=your_jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Install Dependencies

```bash
# Using uv or pip
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn main:app --app-dir app --reload --port 8000
```

Access Swagger interactive documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

### Authentication
- `POST /v1/auth/signup` - Register a new user
- `POST /v1/auth/login` - Authenticate and get tokens
- `POST /v1/auth/refresh` - Refresh access token

### Expenses
- `POST /v1/expenses/add` - Add a new expense
- `GET /v1/expenses/` - List user expenses with optional filters
- `GET /v1/expenses/search?keyword=...` - Search expenses by keyword
- `GET /v1/expenses/summary` - Aggregate spending breakdown
- `PUT /v1/expenses/update/{id}` - Update expense details
- `DELETE /v1/expenses/delete/{id}` - Delete an expense

### AI Agent
- `POST /v1/agent/chat` - Chat with the Copilot to add, list, or summarize expenses

### Health
- `GET /` & `GET /v1/health` - Service health checks
