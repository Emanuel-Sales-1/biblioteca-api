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
- [x] 3. DB connection + SQLAlchemy models — Postgres via `docker-compose`,
      `app/database.py` (engine, `SessionLocal`, `get_db`, `Base`), and all
      models written: `author`, `book` (+ `book_author` association table),
      `copy`, `user`, `loan`
- [ ] 4. CRUD for first entity end-to-end (create/read/update/delete +
      Pydantic validation) — **in progress**
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
Implemented as a plain SQLAlchemy Core `Table` inside `models/book.py`,
alongside the `Book` model.

All 5 entity models (`author`, `book`, `copy`, `user`, `loan`) plus
`book_author` are implemented in `app/models/`. `app/schemas/`,
`app/routers/`, and `app/main.py` are still empty placeholders.

## Infra

Postgres runs locally via Docker Compose (`docker-compose.yml`, single `db`
service, `postgres:16-alpine`, named volume for persistence). Credentials
come from `.env` (gitignored; `.env.example` documents the required keys:
`DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`).

## Current blocker / next step

No blocker. Phase 3 is done — all models exist and were verified to import
and resolve their foreign keys correctly (tables not yet created in
Postgres itself; that'll happen once CRUD needs it, likely via
`Base.metadata.create_all(engine)` or Alembic migrations — not decided
yet). Next concrete step: phase 4, full CRUD (create/read/update/delete +
Pydantic validation) for one entity end-to-end, picking a first entity to
start with.

## Git workflow

One branch per logical unit of work (e.g. `feature/author-model`, not one
branch for the whole phase 3). Each branch gets a PR into `main` with a
Summary/Test plan description, reviewed and merged before starting the
next unit. `delete_branch_on_merge` is enabled on the GitHub repo, so
remote branches clean up automatically after merge — still need
`git branch -d <name>` locally. Commit messages follow Conventional
Commits (`feat: ...`, `fix: ...`, `chore: ...`, `docs: ...`).
