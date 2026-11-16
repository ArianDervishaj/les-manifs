# les-manifs.ch

Agenda collaboratif des manifestations, rassemblements et mobilisations en Suisse.

Les visiteur·euses proposent des événements, les modérateur·ices les valident, tout le
monde consulte l'agenda.

## Lancer le site en local

Python 3.13 requis.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # puis remplir DJANGO_SECRET_KEY
python manage.py migrate
python manage.py createcachetable
python manage.py createsuperuser
python manage.py runserver
```

Le site est sur http://127.0.0.1:8000, l'admin sur http://127.0.0.1:8000/admin/
(l'adresse vient de `DJANGO_ADMIN_URL`).

## Vérifications

```bash
python manage.py test
ruff check . && ruff format --check .
```

Elles tournent aussi automatiquement sur GitHub à chaque push.

## Comme en production (Docker + Caddy)

```bash
docker compose up --build
```

Avec `DOMAIN=localhost` dans `.env`, le site est sur https://localhost (certificat local,
le navigateur affiche un avertissement). La base de données est dans le volume Docker `app_data`.

## Licence

AGPL-3.0. Contact : les-manifs@proton.me
