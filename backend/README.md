# Backend - Tu Merkadito

Backend Django REST Framework para la API de Tu Merkadito.

## Estructura

```
backend/
├── manage.py
├── requirements.txt
├── passenger_wsgi.py
├── .env
├── merkadito/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── api/
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   ├── serializers.py
│   └── models.py
├── businesses/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── products/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
└── analytics/
    ├── __init__.py
    ├── models.py
    ├── views.py
    └── tasks.py
```

## Instalación

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Crear archivo `.env`:

```env
DEBUG=True
SECRET_KEY=django-insecure-local-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=merkadito_local
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306

REDIS_HOST=localhost
REDIS_PORT=6379

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Ejecutar

```bash
python manage.py migrate
python manage.py runserver
```

API disponible en: `http://localhost:8000/api/v1/`
