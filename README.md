# 3awan Cafe & Resto API

Backend REST API untuk aplikasi pemesanan menu restoran.

## Endpoint Utama
- GET /api/menus
- GET /api/categories
- POST /api/orders

## Setup (Windows / PowerShell)

1. Buat virtualenv dan install dependencies:

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Buat file `.env` di root project dengan DATABASE_URL (contoh PostgreSQL):

```
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

Catatan: Aplikasi juga mendukung `RAILWAY_DATABASE_URL` untuk deployment di Railway.

## Deploy
Hosting: Railway  
Database: PostgreSQL (Railway)

3. Buat tabel dan seed data contoh (opsional):

```powershell
& .\venv\Scripts\Activate.ps1
python -c "from app.seed import seed; seed()"
```

4. Jalankan aplikasi dengan uvicorn:

```powershell
& .\venv\Scripts\Activate.ps1
& .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

## API endpoints

- GET /api/categories
- GET /api/menus
- GET /api/menus/{menu_id}
- POST /api/menus
- PUT /api/menus/{menu_id}
- DELETE /api/menus/{menu_id}
- POST /api/orders

## Notes
- Project menggunakan `sqlmodel`. Jangan commit `.env` — berisi kredensial DB.
- Untuk production, siapkan logging dan nonaktifkan debug/echo settings.
