# FastAPI Book App

A production-ready backend service built with FastAPI that allows authenticated users to submit book content and generate AI-powered summaries using an LLM.
The application follows secure configuration practices, async-safe AI calls, JWT-based authentication, and Dockerized deployment.

---

# **Features**

- JWT-based authentication with role-based access control (RBAC)
- AI-powered book summaries using configurable LLM models
- Fully async FastAPI application
- PostgreSQL database with SQLAlchemy ORM
- Complete CRUD APIs for books and summaries
- Environment-based configuration (no hardcoded secrets)
- Structured request/response validation using Pydantic
- Docker & docker-compose support
- Basic test setup aligned with API routes

---
# **Tech Stack**

- Backend: FastAPI
- Database: PostgreSQL (asyncpg)
- ORM: SQLAlchemy 2.x (async)
- Authentication: JWT (OAuth2 password flow)
- AI / LLM: OpenAI (Async client)
- Containerization: Docker, docker-compose
- Testing: Pytest

---

## Project Structure

- book_ai_backend/
- ├── app/
- │ ├── api/
- │ ├── core/
- │ ├── db/
- │ ├── model/
- │ ├── schemas/
- │ ├── services/
- │ ├── unit_test/
- │ └── main.py
- ├── Dockerfile
- ├── docker-compose.yml
- ├── requirement.txt
- ├── .env
- └── README.md

## Setup

### **Clone the repository**

- git clone "<your-repo-url>"
- cd ai_book_summery

### **Create .env file**
- OPENAI_API_KEY ="Enter here"
- SECRET_KEY=add_here
- OPENAI_MODEL=model_name
- OPENAI_MAX_TOKEN=add_here
- POSTGRES_USER=add_here
- POSTGRES_PASSWORD=add_here
- POSTGRES_DB=add_here
- HOST=add_here
- PORT=5432

HOST=db because the FastAPI app and Postgres container share the same Docker network.

### **Start Docker containers**

- docker-compose up --build -d
- API available at "http://localhost:8000"
- Swagger UI "http://localhost:8000/docs"

### **Verify containers are running**

- docker ps

### Docker Commands
- Stop containers
  -  docker-compose down
 
### Run only one test file
- pytest app\unit_test\test_book_service.py -v
- pytest app\unit_test\test_review_service.py -v

---
# Authentication Flow

- Register as a user or admin (only admin has access to create book) 
- Login to receive JWT access token
- Pass token in Authorization header : "Authorization: Bearer <access_token>"

---

# AI Summary Implementation

- Uses async OpenAI client
- Model name and token limits are configurable via env
- Structured responses
- Proper timeout & exception handling
- No blocking calls inside async endpoints


# Security Considerations

- No hardcoded secrets
- JWT tokens securely generated
- Role-based authorization enforced
- Sensitive endpoints protected
- Input validation on all APIs




