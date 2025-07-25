# fastapi_chat_app
# 💬 FastAPI Chat Application

A secure, real-time chat system built with **FastAPI**, featuring:

- ✅ JWT Authentication
- ✅ Role-Based Access Control (RBAC)
- ✅ WebSocket-based messaging
- ✅ PostgreSQL database persistence

---

## 📁 Project Structure

fastapi_chat_app/
├── .env # Environment variables
├── app/ # Application source code
│ ├── init.py # Package initialization
│ ├── config.py # ✅ Group B: Configuration settings
│ ├── database.py # ✅ Group B: Database connection
│ ├── models.py # ✅ Group B: Database models (User, Room, Message)
│ ├── schemas.py # ✅ Group A & B: Pydantic schemas
│ ├── auth.py # ✅ Group A: Authentication (JWT, password hashing)
│ ├── dependencies.py # ✅ Group A: Role-based access (RBAC)
│ ├── chat_websockets.py # ✅ Group A: WebSocket chat handling
│ └── main.py # ✅ Group A & B: FastAPI app entrypoint
├── venv/ # Virtual environment (created during setup)
└── README.md # Project documentation


---

## ✅ Features Implemented

### 🟢 Group A (Mandatory)

- Virtual environment setup and dependency isolation
- JWT Authentication using `python-jose`
- Password hashing using `passlib[bcrypt]`
- Role-based access control (Admin, User roles)
- WebSocket-based real-time chat
- Basic message broadcasting
- Authentication required for WebSocket access

### 🔵 Group B (Task 1 – PostgreSQL Persistence)

- PostgreSQL integration with SQLModel
- User, Room, and Message tables
- Message persistence and retrieval
- Database relationships and foreign keys
- Initial seed data setup (admin, default rooms)

---

## 🧪 Setup & Run

### 1. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Install dependencies

```bash

pip install -r requirements.txt

```
## 3. Create a PostgreSQL database

``` sql
CREATE DATABASE chat_db;
CREATE USER chat_user WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE chat_db TO chat_user;

```

## 4. Create .env file
``` env
DATABASE_URL=postgresql://chat_user:securepassword@localhost:5432/chat_db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


```
## 5. Run the app

``` bash
uvicorn app.main:app --reload

```




