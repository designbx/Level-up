# LevelUp SMMA — Backend API

FastAPI + MySQL backend for the LevelUp Social Media Marketing Agency website.

---

## Features
- ✅ User registration & login (JWT auth)
- ✅ Contact form → saves lead + sends emails
- ✅ Lead management (CRUD, status updates)
- ✅ Admin dashboard stats
- ✅ Email notifications (confirmation + admin alert)

---

## Setup

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create MySQL database
```sql
CREATE DATABASE levelup_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your DB credentials, JWT secret, and SMTP settings
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

API is live at: http://localhost:8000  
Interactive docs: http://localhost:8000/docs

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login (returns JWT) |
| GET  | /api/auth/me | Get current user |
| POST | /api/auth/change-password | Change password |

### Contact
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/contact/ | Submit contact form |

### Leads (Admin only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/leads/ | List all leads |
| GET    | /api/leads/{id} | Get single lead |
| PATCH  | /api/leads/{id}/status | Update lead status |
| DELETE | /api/leads/{id} | Delete lead |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | /api/admin/stats | Dashboard stats |
| GET  | /api/admin/users | List all users |
| PATCH | /api/admin/users/{id}/toggle-admin | Toggle admin role |

---

## Create your first admin user

Register normally via `/api/auth/register`, then run this SQL:
```sql
UPDATE users SET is_admin = 1 WHERE email = 'your@email.com';
```

---

## Gmail SMTP setup
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account → Security → App Passwords
3. Generate a password for "Mail"
4. Use that password as `SMTP_PASSWORD` in your `.env`
