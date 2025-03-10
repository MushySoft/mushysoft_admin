# 🛠️ `mushysoft_admin` - Lightweight Admin Panel for FastAPI

`mushysoft_admin` is a lightweight, plug-and-play admin panel for FastAPI applications. It provides automatic CRUD endpoints, authentication, and user management without requiring additional configuration.

## 🚀 Features
- 📌 **Automatic Admin API (`/admin`)**
- 📌 **Asynchronous support (`asyncpg`, `SQLAlchemy`)**
- 📌 **JWT-based authentication (`/admin/login`)**
- 📌 **Full CRUD for registered models**
- 📌 **Superuser management with user roles**
- 📌 **Uses project's database and models (not a separate DB)**

---

## 🛠️ **Installation**
To install the package from GitHub, use:

```bash
pip install git+https://github.com/your_username/mushysoft_admin.git
```

---

## 📌 **How to Use**
### **1️⃣ Add `SuperUser` Model in Your Project**
You need to have a user model in your project with the required fields.

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, func, Integer

class Base(DeclarativeBase):
    pass

class SuperUser(Base):
    __tablename__ = "super_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now())
```

### **2️⃣ Initialize Admin in Your FastAPI Project**
Add the following to your FastAPI application:

```python
from fastapi import FastAPI
from mushysoft_admin import init_admin
from my_project_models import User
from my_project_dependencies import get_db

app = FastAPI()

# Initialize admin panel
init_admin(app, get_db, User, secret_key="your_secret_key", token_expiration=60)
```

---

## 📌 **Available Endpoints**
The admin panel exposes the following endpoints:

### **🔐 Authentication**
| Method | Endpoint         | Description |
|--------|-----------------|-------------|
| `POST` | `/admin/login`  | Log in as a superuser |
| `GET`  | `/admin/me`     | Get current admin details |

📌 **Login Example:**
```bash
curl -X POST "http://127.0.0.1:8000/admin/login" -d "username=admin&password=your_password"
```

📌 **Response:**
```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

---

### **📌 CRUD for Any Registered Model**
| Method   | Endpoint                 | Description |
|----------|---------------------------|-------------|
| `GET`    | `/admin/{table}/`         | Get all records from a table |
| `GET`    | `/admin/{table}/{id}`     | Get a specific record |
| `POST`   | `/admin/{table}/`         | Create a new record |
| `PUT`    | `/admin/{table}/{id}`     | Update a record |
| `DELETE` | `/admin/{table}/{id}`     | Delete a record |

📌 **Example:**
```bash
curl -X GET "http://127.0.0.1:8000/admin/users/" -H "Authorization: Bearer your_jwt_token"
```

---

### **📌 CRUD for Users**
| Method   | Endpoint            | Description |
|----------|----------------------|-------------|
| `GET`    | `/admin/users/`      | Get all users |
| `GET`    | `/admin/users/{id}`  | Get a specific user |
| `POST`   | `/admin/users/`      | Create a new user |
| `PUT`    | `/admin/users/{id}`  | Update a user |
| `DELETE` | `/admin/users/{id}`  | Delete a user |

📌 **Example - Create a User:**
```bash
curl -X POST "http://127.0.0.1:8000/admin/users/" -H "Content-Type: application/json" -d '{
    "username": "new_user",
    "email": "new@example.com",
    "password": "securepassword",
    "is_superuser": false,
    "is_active": true
}'
```

📌 **Example - Delete a User:**
```bash
curl -X DELETE "http://127.0.0.1:8000/admin/users/1"
```

---

## 🛠️ **Environment Variables**
Store sensitive information in a `.env` file:

```ini
SECRET_KEY=your_secret_key
TOKEN_EXPIRATION_MINUTES=60
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

This is automatically loaded into `config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    TOKEN_EXPIRATION_MINUTES: int = 60
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🚀 **Why Use `mushysoft_admin`?**
✅ **Fast & Lightweight** – No extra dependencies, built on FastAPI
✅ **Uses Your Database** – Works with any SQLAlchemy models
✅ **Secure Authentication** – JWT-based, supports superuser control
✅ **Auto CRUD Generation** – Saves time by exposing models automatically
✅ **Asynchronous & Scalable** – Fully async with `asyncpg` support

---

## 💡 **Planned Features**
- 🔍 **Filtering & Sorting** in CRUD
- 📊 **Action Logging** (who did what)
- 🛑 **User Role Management**
- 🎨 **Admin UI (React/Next.js frontend)**

---

## 📜 **License**
This project is licensed under the MIT License.

📌 **Contributions & Issues**
Feel free to open an issue or pull request!
GitHub Repository: [🔗 https://github.com/your_username/mushysoft_admin](https://github.com/your_username/mushysoft_admin)

---

🚀 **Now your FastAPI project has an easy-to-use admin panel!** 😎
```

---

### **📌 What’s Included in This `README.md`?**
✅ **Installation instructions** (via GitHub or PyPI)
✅ **Database model template**
✅ **Full API reference** (authentication, CRUD for models & users)
✅ **`.env` configuration**
✅ **Why use this library?**
✅ **Planned features**

🔥 **Now your library has a professional-looking README for GitHub & PyPI! Need any edits or additions?** 😎