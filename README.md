# RBAC FastAPI Baseline

Template backend menggunakan FastAPI + PostgreSQL untuk membangun API dengan fitur RBAC (Role Based Access Control) menggunakan prinsip clean architecture dan SOLID.
> Catatan: baseline ini diuji pada Python 3.13.4.

## Struktur Proyek
```
app/
├── api/                # Layer presentasi (routers)
│   ├── deps.py         # Dependency wiring
│   └── routes/         # Endpoint per resources
├── application/        # Use-case/services
├── core/               # Konfigurasi inti & koneksi DB
├── domain/             # Model dan schema domain
├── infrastructure/     # Implementasi repository
└── tests/              # Unit test
```

## Skema Database
File `rbac_schema.sql` menyertakan tabel-tabel roles, permissions, role_permissions, users, dan user_roles yang kompatibel dengan PostgreSQL.

## Menjalankan Aplikasi
1. Buat virtualenv dan install dependensi (versi dipin supaya tersedia wheel Python 3.13 untuk pydantic-core dan psycopg binary):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set variabel environment `DATABASE_URL` sesuai koneksi PostgreSQL (opsional, default sudah disediakan di `config.py` dengan driver `postgresql+psycopg`).
3. Jalankan server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Buka dokumentasi OpenAPI/Swagger di `http://localhost:8000/docs`.

## Menjalankan Test
Gunakan pytest untuk menjalankan unit test:
```bash
pytest
```

## Endpoints Utama
Setiap resource memiliki endpoint CRUD dasar:
- `/roles` – role RBAC
- `/permissions` – permission
- `/users` – pengguna
- `/role-permissions` – relasi role-permission
- `/user-roles` – relasi user-role

Masing-masing mendukung operasi insert, update, delete, get all, dan filter by condition melalui query parameter.
