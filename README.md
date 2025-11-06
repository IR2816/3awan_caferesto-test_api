<<<<<<< HEAD
=======
<<<<<<< HEAD
# 3awan_caferesto-test_api
=======
>>>>>>> d6ae61f (Initial commit: API with CRUD functionality)
# 3awan Cafe & Resto API

Backend REST API untuk aplikasi pemesanan menu restoran.

## Endpoint Utama
- GET /api/menus
- GET /api/categories
- POST /api/orders

## Setup (Windows / PowerShell)

1. Create virtualenv (if not present):

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Create `.env` in project root with DATABASE_URL (Postgres example):

```
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

## Deploy
Hosting: Railway  
Database: PostgreSQL (Railway)

3. Create DB tables and seed example data:

```powershell
& .\venv\Scripts\Activate.ps1
python -c "from app.seed import seed; seed()"
```

4. Run the app with uvicorn:

```powershell
& .\venv\Scripts\Activate.ps1
& .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

API endpoints

- GET /api/categories
- GET /api/menus
- GET /api/menus/{menu_id}
- POST /api/menus
- PUT /api/menus/{menu_id}
- DELETE /api/menus/{menu_id}
- POST /api/orders

Notes
- The project uses `sqlmodel`. Keep `.env` secret — it contains DB credentials.
- For production, configure proper logging and disable debug/echo settings.
<<<<<<< HEAD
=======
>>>>>>> bbd519c (Initial commit: API with CRUD functionality)
>>>>>>> d6ae61f (Initial commit: API with CRUD functionality)
