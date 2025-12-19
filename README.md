# FastAPI Book App

This project is a FastAPI application with PostgreSQL as the database, fully containerized using Docker. It supports authentication, user roles, and persistent data storage.

---

## Requirements

- Docker
- Docker Compose
- Python 3.13 (for local development, optional)
- pip (optional if using Docker)

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

## Setup and Run

1. **Clone the repository**

git clone <your-repo-url>
cd book_ai_backend

2. **Create .env file**

- POSTGRES_USER=-----
- POSTGRES_PASSWORD=-----
- POSTGRES_DB=---
- HOST=db

HOST=db because the FastAPI app and Postgres container share the same Docker network.

3. **Start Docker containers**

- docker-compose up --build -d

4. **Verify containers are running**

- docker ps

## Docker Commands
- Stop containers
  -  docker-compose down
 
## Run only one test file
- pytest app\unit_test\test_book_service.py -v
- pytest app\unit_test\test_review_service.py -v


