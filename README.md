# Clique de Doissin API

API FastAPI + PostgreSQL pour la vitrine de la Clique de Doissin.

## Démarrage rapide

```bash
cd backend
cp .env.example .env
docker compose up -d db
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

- API : <http://localhost:8000>
- Documentation Swagger : <http://localhost:8000/docs>
- Documentation ReDoc : <http://localhost:8000/redoc>
- pgAdmin : <http://localhost:5050>

Pour arrêter les conteneurs : `docker compose down`.
Pour supprimer aussi les données locales : `docker compose down -v`.

## Organisation

- `app/models` : tables SQLAlchemy
- `app/schemas` : validation des entrées/sorties Pydantic
- `app/api` : routes HTTP
- `alembic` : migrations versionnées
- `app/seed.py` : données de démonstration alignées sur le frontend

Les routes d'écriture sont volontairement ouvertes dans cette v0 pour faciliter le
développement local. Avant toute mise en production, ajoute une authentification
administrateur et protège les routes `POST` (puis les futures routes `PATCH` et
`DELETE`).

## Endpoints

- `GET /api/v1/health`
- `GET|POST /api/v1/events`
- `GET|POST /api/v1/members`
- `GET|POST /api/v1/gallery`
- `POST /api/v1/contact`
- `GET /api/v1/contact/messages`

Le frontend React peut utiliser `VITE_API_URL=http://localhost:8000/api/v1`.
