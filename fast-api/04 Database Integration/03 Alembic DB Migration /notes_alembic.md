# Alembic DB Migration — Hands-on Exercise Notes

This is the final step! We put everything together into a complete, hands-on exercise.

Grab your terminal. Here is the practical workflow from start to finish.

## Exercise: Initial migration, then add a new field and create a second migration.

Assumes a basic FastAPI project set up with SQLAlchemy.

### Phase 1: The Starting Point
Define a simple model. In `app/models.py`:
```python
from sqlalchemy import Column, Integer, String
from app.database import Base  # Assuming you have your Base set up

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
```

### Phase 2: The First Migration
1. **Initialize Alembic:**
   ```bash
   alembic init alembic
   ```
2. **Configure:**
   * Open `alembic.ini` and set `sqlalchemy.url = sqlite:///./test.db` (using SQLite for this exercise).
   * Open `alembic/env.py`, import `Base` from `app.models`, and set `target_metadata = Base.metadata`.
3. **Generate the migration:**
   ```bash
   alembic revision --autogenerate -m "create items table"
   ```
4. **Verify & Apply:**
   * Open the generated file in `alembic/versions/` and confirm it has `op.create_table('items'...)`.
   ```bash
   alembic upgrade head
   ```
   *(Your database now has an `items` table with `id` and `title`.)*

### Phase 3: The Change
Product manager says, *"Items need a description!"*
Open `app/models.py` and update the model:
```python
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    # --- NEW FIELD ---
    description = Column(String, nullable=True)
```

### Phase 4: The Second Migration
1. **Generate the second migration:**
   ```bash
   alembic revision --autogenerate -m "add description to items"
   ```
2. **Verify & Apply:**
   * Open the new file. Confirm it has `op.add_column('items', sa.Column('description'...))`.
   ```bash
   alembic upgrade head
   ```

### Phase 5: Sanity Check
Prove it worked and Alembic is tracking it:
```bash
alembic current
```
*Output:* prints the ID of the second migration, proving DB is up to date.

```bash
alembic history
```
*Output:* a timeline:
```text
<rev2> (head) -> add description to items
<rev1> -> create items table
```

---

## What we actually did in this project
- `uv add alembic` then `alembic init alembic`.
- Configured `alembic.ini` (`sqlalchemy.url = sqlite:///./test.db`) and `alembic/env.py` (`target_metadata = Base.metadata`, `prepend_sys_path = .`).
- First migration `59a305a0b039` — create items table.
- Added `description` to model, second migration `1b21bab56493` — add description to items.
- `alembic upgrade head` applied both; `alembic current` → `1b21bab56493 (head)`; `alembic history` showed the chain. `test.db` created.

## Recap of concepts
1. **Why migrate** — to evolve schema without destroying production data.
2. **How Alembic tracks state** — the `alembic_version` table records the current revision.
3. **Set it up** — `alembic init`, configure `alembic.ini` + `env.py`.
4. **Generate** — `alembic revision --autogenerate -m "..."`.
5. **Apply** — `alembic upgrade head`.
6. **Rollback** — `alembic downgrade -1` (or a specific revision).
7. **Detect new columns** — autogenerate diffs `Base.metadata` vs DB and emits `op.add_column`.
8. **Read generated files** — each version has `upgrade()` / `downgrade()` with `op.*` calls.
9. **Merge conflicts** — multiple heads resolved with `alembic merge heads`.
