# Alembic Cheat Sheet

## Setup
```bash
pip install alembic            # install
alembic init alembic           # scaffold (creates alembic/, alembic.ini, env.py)
```

## Config (one-time)
- `alembic.ini` → set `sqlalchemy.url = sqlite:///./test.db`
- `alembic/env.py` → import your `Base`, set `target_metadata = Base.metadata`
- `alembic.ini` → `prepend_sys_path = .` so env.py can import models

## Generate migrations
```bash
alembic revision -m "message"                  # empty migration
alembic revision --autogenerate -m "message"   # diff models vs DB
```

## Apply / rollback
```bash
alembic upgrade head        # apply all pending
alembic upgrade <rev>       # apply up to a specific revision
alembic downgrade -1        # roll back one step
alembic downgrade <rev>     # roll back to a revision (exclusive)
alembic upgrade +2          # forward 2 steps
alembic downgrade base      # full reset to nothing
```

## Inspect
```bash
alembic current             # current revision in DB
alembic history             # full timeline
alembic heads               # all head revisions
alembic show <rev>          # show one migration's code
alembic check               # autogenerate would produce changes? (CI)
```

## Multiple heads / merges
```bash
alembic merge heads -m "merge"     # combine multiple heads into one
alembic upgrade head               # after merge
```

## Edit generated file (manual override)
Inside `alembic/versions/<rev>_*.py`:
```python
def upgrade() -> None:
    op.execute("SELECT 1;")  # raw SQL injection
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'email')
```
Common `op.*` calls: `op.create_table`, `op.drop_table`, `op.add_column`, `op.drop_column`, `op.create_index`, `op.create_foreign_key`, `op.alter_column`.

## Verify DB directly (SQLite)
```bash
python -c "import sqlite3; c=sqlite3.connect('test.db'); print(c.execute(\"SELECT name FROM sqlite_master WHERE type='table';\").fetchall())"
```

## Typical workflow
1. Edit model in `models.py`
2. `alembic revision --autogenerate -m "what changed"`
3. Open the file, verify `upgrade()` / `downgrade()` are correct
4. `alembic upgrade head`
5. `alembic current` / `alembic history` to confirm

## Common gotchas
- Autogenerate only detects changes tracked by `Base.metadata` — import all models before generating.
- No `target_metadata` → empty migrations (nothing detected).
- SQLite can't `ALTER COLUMN` / `DROP COLUMN` easily — sometimes needs batch mode `with op.batch_alter_table('t') as b:`.
- `downgrade` is NOT auto-generated perfectly for complex changes — review it.
- Don't edit applied migrations; make a new revision instead.
