# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A Django site for learning Japanese ("HTM Japanese"). The Django project is `htm_japanese`, and it currently has a single app, `blogs`, which serves blog posts tagged by topic (anime, food, travel, etc.) and by JLPT grammar point. All project code lives under `japanese_website/`; the repo root only otherwise contains the `venv/` virtualenv.

## Environment setup

- Python 3.12, Django 6.0.5, with a Postgres backend (`psycopg2-binary`) and Pillow for image fields.
- Activate the existing virtualenv before running any commands: `source venv/bin/activate` (run from the repo root).
- Config is read from `japanese_website/.env` via `python-dotenv` (`DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`). A local Postgres instance with a database matching `DB_NAME` must be running for any `manage.py` command that touches the DB.

## Common commands

All `manage.py` commands are run from `japanese_website/`:

```bash
cd japanese_website
python manage.py runserver          # dev server
python manage.py migrate            # apply migrations
python manage.py makemigrations     # after changing blogs/models.py
python manage.py test               # run tests (blogs/tests.py, currently empty)
python manage.py test blogs         # run tests for the blogs app only
python manage.py createsuperuser    # needed to use /admin/ to add Blog entries
```

There is no lint/format tooling configured in this repo.

## Architecture

- **`htm_japanese/`** — the Django project package: `settings.py` (DB config, installed apps, static/media config), root `urls.py` (mounts `blogs.urls` under `/blogs/`, plus `/admin/`, plus media file serving), `wsgi.py`/`asgi.py`.
- **`blogs/`** — the single app, following standard Django layout (`models.py`, `views.py`, `urls.py`, `admin.py`, `templates/blogs/`, `static/blogs/`).
  - `models.Blog` is the sole model. It uses Postgres-specific `ArrayField` (via `django.contrib.postgres`) for `tags` and `grammars`, each constrained by a large hardcoded `choices` list (`TAG_CHOICES`, `GRAMMAR_CHOICES`) defined inline on the model — extend these lists rather than switching field types when adding new categories/grammar points, to keep `category`/grammar filtering views working. `jlpt_level` is a separate single-value choice field (N1–N5). `banner_image` is an `ImageField` uploaded to `blog_banner/` under `MEDIA_ROOT` (`japanese_website/media/`), defaulting to `default/japan-banner.jpg`.
  - `views.py` has three view functions: `index` (latest 10 blogs by `pub_date`), `content` (single blog by pk), `category` (filters `Blog.objects.filter(tags__contains=tag)`, 404s on an unrecognized tag). A fourth function, `grammer`, filters by `grammars__contains` but is not currently wired into `urls.py`/`urlpatterns` — it's a work in progress, not a dead route to "fix" by removing.
  - `urls.py` in the app only defines routes for `index`, `content`, and `category`; there is no grammar-browsing URL yet even though the template (`grammar.html`) and view (`grammer`) exist.
  - Blog content is entered through the Django admin (`Blog` is registered in `admin.py`) rather than through any custom authoring UI.
