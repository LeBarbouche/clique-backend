# La Clique de Doissin

Backend et frontend du site vitrine de La Clique de Doissin.

Le projet fournit :

- une vitrine publique pour les actualités, les événements, la galerie et les membres ;
- un formulaire de contact ;
- une authentification par jeton Bearer ;
- trois rôles d’accès : `superadmin`, `admin` et `utilisateur` ;
- une gestion des actualités ;
- des commentaires authentifiés sur les actualités, les photos et les événements ;
- une base PostgreSQL versionnée avec Alembic ;
- une interface pgAdmin optionnelle pour administrer la base.

## Sommaire

1. [Architecture](#architecture)
2. [Prérequis](#prérequis)
3. [Installation rapide](#installation-rapide)
4. [Démarrer le projet](#démarrer-le-projet)
5. [Configuration](#configuration)
6. [PostgreSQL et pgAdmin](#postgresql-et-pgadmin)
7. [Base de données et migrations](#base-de-données-et-migrations)
8. [Compte initial](#compte-initial)
9. [Authentification et rôles](#authentification-et-rôles)
10. [API](#api)
11. [Exemples d’utilisation](#exemples-dutilisation)
12. [Frontend](#frontend)
13. [Validation](#validation)
14. [Dépannage](#dépannage)
15. [Production](#production)

## Architecture

```text
site-musique/
├── backend/
│   ├── app/
│   │   ├── api/              # Dépendances et routes FastAPI
│   │   ├── core/             # Configuration de l’application
│   │   ├── db/               # Engine et sessions SQLAlchemy
│   │   ├── models/           # Modèles SQLAlchemy
│   │   ├── schemas/          # Schémas Pydantic
│   │   ├── main.py           # Application FastAPI
│   │   └── seed.py           # Données de démonstration
│   ├── alembic/              # Migrations de base de données
│   ├── docker-compose.yml    # PostgreSQL et pgAdmin
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── api/              # Client HTTP centralisé
    │   ├── auth/             # Session et utilisateur courant
    │   ├── components/       # Composants visuels
    │   ├── pages/            # Pages React
    │   ├── types/            # Types TypeScript
    │   └── data/             # Données éditoriales locales non migrées
    ├── package.json
    └── .env.example
```

### Technologies

| Couche | Technologies |
| --- | --- |
| Frontend | React 19, TypeScript strict, Vite, React Router |
| Backend | FastAPI, Pydantic 2, SQLAlchemy 2 |
| Base de données | PostgreSQL 16 |
| Migrations | Alembic |
| Conteneurs | Docker Compose |
| Administration DB | pgAdmin 4 optionnel |

## Prérequis

- Docker et Docker Compose ;
- Python 3.11 ou supérieur ;
- Node.js 18 ou supérieur et npm ;
- Git ;
- un navigateur récent.

Vérifier les outils :

```bash
docker --version
docker compose version
python3 --version
node --version
npm --version
```

## Installation rapide

Depuis le dossier du projet :

```bash
cd /home/barbouche/Documents/site-musique
```

### 1. Configurer le backend

```bash
cd backend
cp .env.example .env
```

Générer un secret suffisamment long :

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

Remplacer ensuite la valeur de `AUTH_SECRET` dans `backend/.env`.

### 2. Préparer Python

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Sous Windows PowerShell, l’activation correspondante est :

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Démarrer PostgreSQL

```bash
docker compose up -d db
```

### 4. Initialiser la base

```bash
alembic upgrade head
python -m app.seed
```

Le seed est volontairement idempotent au niveau de la présence d’événements : il
ne faut pas le lancer comme mécanisme de migration. Les changements de structure
doivent toujours passer par Alembic.

### 5. Installer le frontend

```bash
cd ../frontend
npm install
cp .env.example .env
```

## Démarrer le projet

Ouvrir deux terminaux.

### Terminal backend

```bash
cd /home/barbouche/Documents/site-musique/backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

URLs disponibles :

- API : <http://localhost:8000>
- Health check : <http://localhost:8000/api/v1/health>
- Swagger UI : <http://localhost:8000/docs>
- ReDoc : <http://localhost:8000/redoc>

### Terminal frontend

```bash
cd /home/barbouche/Documents/site-musique/frontend
npm run dev
```

URL habituelle : <http://localhost:5173>

Si le port est déjà occupé, Vite choisit automatiquement un autre port, par
exemple <http://localhost:5174>.

## Configuration

### Backend : `backend/.env`

```dotenv
APP_NAME=Clique de Doissin API
APP_ENV=development
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/clique_doissin
CORS_ORIGINS=http://localhost:5173
AUTH_SECRET=remplacer-par-un-secret-aleatoire-dau-moins-32-caracteres
AUTH_TOKEN_EXPIRE_MINUTES=1440
```

`AUTH_SECRET` est obligatoire et doit contenir au moins 32 caractères. Il ne doit
jamais être commité ni exposé dans une réponse API.

Pour plusieurs origines frontend, séparer les valeurs par des virgules :

```dotenv
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

### Frontend : `frontend/.env`

```dotenv
VITE_API_URL=http://localhost:8000/api/v1
```

Le frontend ne connaît jamais la base de données. Il communique uniquement avec
l’API HTTP via `src/api/client.ts`.

## PostgreSQL et pgAdmin

### PostgreSQL avec Docker

Voir l’état des services :

```bash
cd backend
docker compose ps
```

Ouvrir une console PostgreSQL directement dans le conteneur :

```bash
docker compose exec db psql -U postgres -d clique_doissin
```

Commandes utiles dans `psql` :

```sql
\dt
\d news_articles
SELECT id, title, published FROM news_articles;
SELECT id, email, role FROM users;
\q
```

### pgAdmin en conteneur

Lancer pgAdmin :

```bash
docker compose --profile tools up -d pgadmin
```

Ouvrir <http://localhost:5050> avec :

- email : `admin@clique-doissin.fr` ;
- mot de passe : `admin`.

Dans pgAdmin, enregistrer un serveur avec les paramètres suivants :

| Champ | Valeur |
| --- | --- |
| Name | `Clique de Doissin` |
| Host name/address | `db` |
| Port | `5432` |
| Maintenance database | `clique_doissin` |
| Username | `postgres` |
| Password | `postgres` |

Lorsque pgAdmin est lui-même exécuté dans Docker, le hostname doit être `db` :
`localhost` désignerait le conteneur pgAdmin lui-même.

### pgAdmin installé directement sur l’ordinateur

Si pgAdmin n’est pas le conteneur Docker mais une application installée sur la
machine, utiliser :

| Champ | Valeur |
| --- | --- |
| Host name/address | `localhost` |
| Port | `5432` |
| Maintenance database | `clique_doissin` |
| Username | `postgres` |
| Password | `postgres` |

Le port `5432` est publié par Docker sur la machine hôte.

### Arrêter les services

```bash
docker compose stop
```

Supprimer les conteneurs sans supprimer les données :

```bash
docker compose down
```

Supprimer également le volume PostgreSQL et toutes les données locales :

```bash
docker compose down -v
```

Cette dernière commande est destructive.

## Base de données et migrations

Les tables principales sont :

- `users` : comptes et rôles ;
- `news_articles` : actualités publiées ou brouillons ;
- `events` : calendrier ;
- `gallery_photos` : galerie ;
- `members` : membres de la clique ;
- `comments` : commentaires polymorphes sur les actualités, photos et événements ;
- `contact_messages` : messages du formulaire de contact.

Voir la migration courante :

```bash
alembic current
```

Voir l’historique :

```bash
alembic history
```

Appliquer les migrations :

```bash
alembic upgrade head
```

Créer une migration après une modification de modèle :

```bash
alembic revision --autogenerate -m "describe the change"
```

Toujours relire et tester une migration auto-générée avant de l’utiliser.

## Compte initial

Le seed crée le compte suivant :

```text
Email        : superadmin@clique-doissin.fr
Mot de passe : change-me-please
Rôle         : superadmin
```

Ce compte est uniquement destiné au démarrage local. Son mot de passe doit être
changé avant toute utilisation réelle. Le mot de passe n’est jamais renvoyé par
l’API.

## Authentification et rôles

La connexion se fait avec `POST /api/v1/auth/login`. La réponse contient un jeton
Bearer et les informations publiques de l’utilisateur :

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "superadmin@clique-doissin.fr",
    "display_name": "Super administrateur",
    "role": "superadmin",
    "is_active": true,
    "created_at": "2026-09-13T12:00:00Z"
  }
}
```

Envoyer ensuite le jeton avec :

```http
Authorization: Bearer <access_token>
```

### Matrice des permissions

| Fonction | Public | `utilisateur` | `admin` | `superadmin` |
| --- | ---: | ---: | ---: | ---: |
| Lire les événements | Oui | Oui | Oui | Oui |
| Lire les photos | Oui | Oui | Oui | Oui |
| Lire les membres | Oui | Oui | Oui | Oui |
| Lire les actualités publiées | Oui | Oui | Oui | Oui |
| Envoyer un contact | Oui | Oui | Oui | Oui |
| Lire les messages de contact | Non | Non | Oui | Oui |
| Créer/modifier/supprimer contenu | Non | Non | Oui | Oui |
| Publier un commentaire | Non | Oui | Oui | Oui |
| Modérer/supprimer un commentaire | Non | Non | Oui | Oui |
| Créer des comptes | Non | Non | Non | Oui |
| Lister les comptes | Non | Non | Non | Oui |

Le frontend peut masquer une action selon le rôle, mais la sécurité réelle est
toujours contrôlée par le backend.

## API

Préfixe général : `/api/v1`.

### Système

| Méthode | Route | Accès | Description |
| --- | --- | --- | --- |
| `GET` | `/health` | Public | Vérifie que l’API répond |

### Authentification

| Méthode | Route | Accès | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/login` | Public | Connexion |
| `GET` | `/auth/me` | Authentifié | Utilisateur courant |
| `GET` | `/auth/users` | Superadmin | Liste des comptes |
| `POST` | `/auth/users` | Superadmin | Crée un compte |

### Contenu

| Ressource | Lecture | Création | Modification | Suppression |
| --- | --- | --- | --- | --- |
| Événements | `GET /events` | `POST /events` | `PUT /events/{id}` | `DELETE /events/{id}` |
| Membres | `GET /members` | `POST /members` | `PUT /members/{id}` | `DELETE /members/{id}` |
| Photos | `GET /gallery` | `POST /gallery` | `PUT /gallery/{id}` | `DELETE /gallery/{id}` |
| Actualités | `GET /news` | `POST /news` | `PUT /news/{id}` | `DELETE /news/{id}` |

Les créations, modifications et suppressions de contenu nécessitent un rôle
`admin` ou `superadmin`. `GET /news` ne retourne que les articles publiés.

### Commentaires

| Méthode | Route | Accès | Description |
| --- | --- | --- | --- |
| `GET` | `/comments/{content_type}/{content_id}` | Public | Liste les commentaires |
| `POST` | `/comments` | Authentifié | Ajoute un commentaire |
| `DELETE` | `/comments/{comment_id}` | Admin ou superadmin | Supprime un commentaire |

`content_type` doit être `news`, `photo` ou `event`. La création vérifie que la
ressource ciblée existe et renvoie `404` sinon.

### Contact

| Méthode | Route | Accès | Description |
| --- | --- | --- | --- |
| `POST` | `/contact` | Public | Envoie un message |
| `GET` | `/contact/messages` | Admin ou superadmin | Liste les messages |

## Exemples d’utilisation

### Vérifier l’API

```bash
curl http://localhost:8000/api/v1/health
```

Réponse attendue :

```json
{"status":"ok"}
```

### Se connecter

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "superadmin@clique-doissin.fr",
    "password": "change-me-please"
  }'
```

Conserver la valeur `access_token` retournée et l’utiliser dans les requêtes
protégées.

### Lire les actualités

```bash
curl http://localhost:8000/api/v1/news
```

### Créer une actualité

```bash
curl -X POST http://localhost:8000/api/v1/news \
  -H 'Authorization: Bearer VOTRE_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Répétition ouverte",
    "slug": "repetition-ouverte",
    "content": "Venez découvrir la clique.",
    "image_url": null,
    "published": true
  }'
```

### Ajouter un commentaire

```bash
curl -X POST http://localhost:8000/api/v1/comments \
  -H 'Authorization: Bearer VOTRE_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "content_type": "news",
    "content_id": 1,
    "body": "Bravo pour cette nouvelle saison !"
  }'
```

### Envoyer un message de contact

```bash
curl -X POST http://localhost:8000/api/v1/contact \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Marie Dupont",
    "email": "marie@example.com",
    "message": "Bonjour, pouvez-vous jouer pour notre événement ?"
  }'
```

## Frontend

Le frontend se trouve dans `/home/barbouche/Documents/site-musique/frontend`.

### Commandes

```bash
cd frontend
npm install
npm run dev
```

Contrôles qualité :

```bash
npm run lint
npm run build
```

### Fonctionnalités connectées

- actualités depuis `GET /news` ;
- agenda depuis `GET /events` ;
- galerie depuis `GET /gallery` ;
- membres depuis `GET /members` ;
- connexion depuis `POST /auth/login` ;
- récupération de session depuis `GET /auth/me` ;
- commentaires d’actualités depuis `/comments` ;
- formulaire de contact depuis `POST /contact` ;
- création, modification et suppression d’actualités dans l’espace de gestion.

Le token est stocké dans le stockage local du navigateur. La déconnexion le
supprime. Un token expiré ou invalide entraîne automatiquement la suppression de
la session locale.

## Validation

### Backend

```bash
cd backend
source .venv/bin/activate
docker compose up -d db
alembic upgrade head
python -m app.seed
python -m compileall -q app alembic
uvicorn app.main:app --reload
```

Vérifier ensuite :

```bash
curl http://localhost:8000/api/v1/health
curl -I http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm run lint
npm run build
npm run dev
```

### Vérifications fonctionnelles recommandées

1. Ouvrir `/gestion` et se connecter avec le compte superadmin.
2. Vérifier l’affichage des actualités, de l’agenda, de la galerie et des membres.
3. Ouvrir une actualité et publier un commentaire connecté.
4. Vérifier qu’un utilisateur `utilisateur` reçoit `403` lors d’une action admin.
5. Envoyer le formulaire de contact et contrôler `contact_messages` dans PostgreSQL.
6. Créer puis modifier une actualité depuis `/gestion`.
7. Vérifier que les contenus absents affichent un état vide et que les erreurs API
   sont visibles sans casser la page.

## Dépannage

### `connection refused` sur PostgreSQL

Vérifier le conteneur et le port :

```bash
docker compose ps
nc -vz localhost 5432
```

Depuis une application installée sur l’hôte, utiliser `localhost` comme hostname.
Depuis pgAdmin exécuté dans Docker, utiliser `db`.

### pgAdmin redémarre en boucle

Lire les logs :

```bash
docker compose logs --tail=100 pgadmin
```

Lancer le profil tools :

```bash
docker compose --profile tools up -d pgadmin
```

L’email configuré doit être valide : `admin@clique-doissin.fr`.

### Le frontend ne joint pas l’API

Vérifier `frontend/.env` :

```dotenv
VITE_API_URL=http://localhost:8000/api/v1
```

Vérifier également que FastAPI tourne sur le port `8000` et que `CORS_ORIGINS`
contient l’origine réellement utilisée par Vite.

### `AUTH_SECRET` manquant ou trop court

Définir une valeur d’au moins 32 caractères dans `backend/.env` :

```dotenv
AUTH_SECRET=une-valeur-aleatoire-longue-et-non-commitee
```

### Les changements de modèles ne sont pas visibles

Les modèles Python ne modifient pas automatiquement la base. Créer puis appliquer
une migration :

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

### Réinitialiser complètement la base locale

Attention, cette procédure supprime toutes les données :

```bash
docker compose down -v
docker compose up -d db
alembic upgrade head
python -m app.seed
```

## Production

Avant une mise en production :

- remplacer le mot de passe PostgreSQL par un secret dédié ;
- générer un `AUTH_SECRET` aléatoire et privé ;
- remplacer le mot de passe du compte superadmin ;
- ne pas utiliser les identifiants pgAdmin `admin` par défaut ;
- limiter `CORS_ORIGINS` aux domaines frontend autorisés ;
- servir l’API et le frontend derrière HTTPS ;
- ne pas exposer directement PostgreSQL à Internet ;
- sauvegarder le volume PostgreSQL ;
- appliquer les migrations avant le déploiement de l’application ;
- désactiver ou protéger fortement pgAdmin ;
- ajouter une vraie gestion de rotation/révocation des tokens si nécessaire ;
- mettre en place des logs, alertes et tests automatisés.

Les valeurs présentes dans `docker-compose.yml` sont adaptées au développement
local, pas à un environnement de production.

## État du projet

Le backend expose le CRUD protégé pour les actualités, événements, membres et
photos. Le frontend utilise actuellement l’API pour les lectures publiques, la
connexion, les commentaires d’actualités, le contact et la gestion des actualités.
Les écrans frontend dédiés à la gestion des photos, événements et membres restent
à développer ; leurs routes backend existent déjà.
