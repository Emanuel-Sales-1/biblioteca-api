# PROGRESS.md

Source of truth for where this project stands. Read this before resuming work.

## Goal

Backend portfolio project targeting a backend development internship. This is
"Project 1" of a 3-project portfolio plan (CRUD API → web scraper/pipeline →
API with auth). Full idea list: `random-stuff/ideias-projetos-portfolio.md`
in the user's workspace (outside this repo).

## Working mode

**Mentor mode.** The user writes all implementation code themselves; the
assistant explains concepts, reviews code, asks guiding questions, and only
writes non-educational boilerplate (config files, folder scaffolding,
docs) when explicitly asked. Do not write CRUD/business logic for the user.

## Stack

- FastAPI (chosen over Flask for built-in validation + auto docs)
- PostgreSQL (chosen over MySQL/SQLite — better free-tier support on
  Render/Railway/Fly.io for the eventual deploy phase)
- SQLAlchemy (ORM)
- `uv` for venv/dependency management (compatible mode: `uv venv` +
  `requirements.txt`, not the native `pyproject.toml`/lockfile mode — chosen
  to keep `pip install -r requirements.txt` working for anyone without `uv`)
- All code, entity names, and docs in **English** (decided explicitly,
  applied 2026-08-18 before any real logic was written)

## Domain

Library management system (books, authors, users, copies, loans).

## Phase plan (8 phases, from the original portfolio checklist)

- [x] 0. Choose domain — library system
- [x] 1. DB modeling — see `docs/schema.dbml`
- [x] 2. Project setup — repo, `.gitignore`, venv, `requirements.txt`, folder
      structure, first commit (`e4aa772`)
- [ ] 3. DB connection + SQLAlchemy models — **in progress**, currently
      setting up local PostgreSQL
- [ ] 4. CRUD for first entity end-to-end (create/read/update/delete +
      Pydantic validation)
- [ ] 5. Relationships between entities
- [ ] 6. Pagination and queries
- [ ] 7. Tests with pytest
- [ ] 8. README (real content, currently a placeholder) + free deploy
      (Render/Railway/Fly.io)

Each phase ends with a commit + review before moving to the next.

## Data model — key decisions and reasoning

Entities: `book`, `author`, `user`, `copy`, `loan`, plus `book_author`
(pure association table for the book↔author N:N).

- **`book` vs `copy`**: `book` is the title/edition; `copy` is one physical
  copy (`book` 1:N `copy`). Chosen deliberately (option B over a simpler
  "book = single copy" model) for realism.
- **`book` ↔ `author`**: N:N, resolved via `book_author` junction table with
  a **composite primary key** `(author_id, book_id)` — needed to prevent
  duplicate rows, since a plain FK column can't hold multiple values per row.
- **`loan`**: associative entity between `user` and `copy` (same N:N-over-time
  reasoning as `book_author` — one user has many loans over time, one copy is
  loaned to many different users over time).
- **Availability is not a stored field.** Decided against a `status` column
  on `copy` (would be derived/duplicated data, risk of going stale). Instead,
  availability is inferred by querying `loan` for a row with that `copy_id`
  and `return_date IS NULL`.
- **No ISBN field on `book`.** Explicit decision to skip it — remember to
  note this decision in the README when writing it in phase 8.
- **No "condition/state" field on `copy`.** Cut deliberately — not used by
  any business rule defined so far (YAGNI); can be added later via migration
  if a rule ever needs it.
- **FK naming convention**: suffix style (`book_id`, `author_id`, `copy_id`,
  `user_id`), not prefix — idiomatic for English/SQLAlchemy code, even
  though the very first (Portuguese) draft used prefix style.
- Full schema lives in `docs/schema.dbml` (paste into dbdiagram.io to view).

## Project structure

```
app/
├── main.py              # FastAPI app instance, includes routers
├── database.py           # engine, session, get_db dependency
├── models/                # SQLAlchemy classes, one file per entity
├── schemas/               # Pydantic classes, one file per entity
└── routers/               # APIRouter per entity, plural filenames (REST convention)
docs/schema.dbml           # DB schema (DBML)
tests/
```

`book_author` intentionally has **no** model/schema/router file of its own —
it's a pure junction table (no own identity, no REST endpoints of its own).
It should be defined as a plain SQLAlchemy `Table`, not a full model class,
likely inside `database.py` or `models/book.py` (not yet implemented).

All `app/*` files are currently empty placeholders — content is written
phase by phase, by the user.

## Current blocker / next step

Setting up local PostgreSQL before phase 3 can start. Decided to use
**Docker** (not installed yet on this machine) over a native `pacman`
install, for isolation and because container experience is a relevant skill
to demonstrate. Next concrete step: install Docker, then run a Postgres
container, then start phase 3 (SQLAlchemy `database.py` + first model).
