# E-Commerce Platform

A full-stack e-commerce application with a **React.js** frontend (Axios, React Router) and a **Python / Tornado** REST backend on **MySQL**.

## Features
- User registration and login. Passwords are stored as **bcrypt hashes**.
- Signed, expiring login tokens. The server identifies users from the token and never trusts a `user_id` sent by the client.
- Role-based access: the admin product endpoints check the user's role in the database. Public sign-up always creates a normal user; admins are promoted by the site owner with a script.
- Product catalogue, plus admin add / edit / delete.
- Shopping cart: each user can only read or change their own cart. Guest carts are kept in the browser.

## Tech stack
React 19 · Axios · React Router · Python 3 · Tornado · PyMySQL · bcrypt · MySQL/MariaDB

## Setup

### 1. Database
```bash
mysql -u root -p < backend/sql/schema.sql
# Create a dedicated, least-privilege database user (don't use root):
mysql -u root -p -e "CREATE USER 'ecommerce_app'@'localhost' IDENTIFIED BY '<strong-password>';
                     GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.* TO 'ecommerce_app'@'localhost';"
```

### 2. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then edit .env: DB credentials + a random APP_SECRET
python app.py               # http://localhost:8888
```
Create the first admin (after registering normally in the app):
```bash
python scripts/make_admin.py you@example.com
```

### 3. Frontend
```bash
cd frontend
npm install
npm start                   # http://localhost:3000
```

## Upgrading an existing database
If your database was created by an earlier version, which stored plain-text passwords:
```sql
ALTER TABLE user_details MODIFY password VARCHAR(255) NOT NULL;
```
```bash
python scripts/migrate_hash_passwords.py
```

## API
| Method | Path | Auth |
|---|---|---|
| POST | /register | public |
| POST | /login | public, returns a token |
| GET | /products | public |
| POST / PUT / DELETE | /admin/product/add · /edit · /delete | admin token |
| POST | /cart/add | user token |
| GET | /cart/{user_id} | user token (own cart only) |
| DELETE | /cart | user token |

Send the token as `Authorization: Bearer <token>`.
