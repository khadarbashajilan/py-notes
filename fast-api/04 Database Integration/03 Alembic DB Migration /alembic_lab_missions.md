# Alembic Local Lab — Hands-On Missions

I love this approach. Reading about it is one thing, but building the "muscle memory" is what makes you a confident backend developer.

Let's do a **Hands-On Local Lab**. Open your terminal right now, create a fresh folder, and follow these 3 Missions.

To make this frictionless, we use SQLite so you don't need to install Postgres.

### The Quick Setup (Copy & Paste)
Create a new folder, initialize a virtual environment, and install the tools:
```bash
mkdir alembic_lab && cd alembic_lab
python -m venv venv
# Activate it (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install fastapi sqlalchemy alembic uvicorn
```

Create these two files in your root folder:

**`database.py`**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./lab.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
```

**`models.py`**
```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
```

Initialize Alembic:
```bash
alembic init alembic
```
*Crucial step:* Open `alembic/env.py`, add `from database import Base` at the top, and change `target_metadata = None` to `target_metadata = Base.metadata`.
Also, open `alembic.ini` and change the URL to: `sqlalchemy.url = sqlite:///./lab.db`

---

### Mission 1: The "Time Traveler" (Upgrade & Downgrade Loop)
*Goal: Watch Alembic track the state of the database forward and backward.*

1. **Generate & Apply:**
   ```bash
   alembic revision --autogenerate -m "create users"
   alembic upgrade head
   ```
2. **Observe the DB:** Run this quick python command to see what tables exist:
   ```bash
   python -c "import sqlite3; conn=sqlite3.connect('lab.db'); print(conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\";').fetchall())"
   ```
   *(You should see `['alembic_version', 'users']`)*
3. **Check Alembic's Brain:**
   ```bash
   alembic current
   ```
   *(It will print the ID of the "create users" migration).*
4. **Time Travel (Rollback):**
   ```bash
   alembic downgrade -1
   ```
5. **Observe the DB again:** Run that exact same `python -c ...` command from Step 2.
   *(The `users` table is GONE. Only `alembic_version` remains).*
6. **Go back to the future:**
   ```bash
   alembic upgrade head
   ```

---

### Mission 2: The "Manual Override" (Editing a Migration)
*Goal: Prove that you are the boss of the migration file, not Alembic.*

1. **Change the model:** Open `models.py` and add an `email` column to the `User` class:
   ```python
   email = Column(String, unique=True)
   ```
2. **Autogenerate:**
   ```bash
   alembic revision --autogenerate -m "add email"
   ```
3. **The Override:** Open the newly generated file in `alembic/versions/`.
   Find the `upgrade()` function. Right above the `op.add_column` line, add this raw SQL command:
   ```python
   def upgrade() -> None:
       op.execute("SELECT 1;") # <--- I just added raw SQL!
       op.add_column('users', sa.Column('email', sa.String(), nullable=True))
   ```
4. **Apply it:**
   ```bash
   alembic upgrade head
   ```
5. **Observe:** Run `alembic history`. You will see your manual edit didn't break anything. Alembic just executed your raw SQL along with its Python commands. You now know how to inject custom SQL into migrations!

---

### Mission 3: The "Relationship" (Foreign Keys)
*Goal: See how Alembic handles linking two tables together.*

1. **Add a new model:** Open `models.py` and add a `Post` model at the bottom:
   ```python
   from sqlalchemy import ForeignKey

   class Post(Base):
       __tablename__ = "posts"
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, index=True)
       # This links the Post to the User!
       owner_id = Column(Integer, ForeignKey("users.id"))
   ```
2. **Autogenerate:**
   ```bash
   alembic revision --autogenerate -m "create posts with foreign key"
   ```
3. **Read the file:** Open the new migration file. Look closely at the `upgrade()` function. You will see `op.create_table` for posts, but look at the `owner_id` column definition. You will see `sa.ForeignKeyConstraint(['owner_id'], ['users.id'])`. Alembic automatically figured out the relationship!
4. **Apply it:**
   ```bash
   alembic upgrade head
   ```
5. **Final Check:** Run `alembic history`. You should now see a beautiful, clean timeline of 3 migrations.

---

**Go run these missions!** Once you do this, you will never be scared of Alembic again.
