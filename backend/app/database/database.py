from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
from app.core.config import settings

# For SQLite, check_same_thread is required to allow multiple threads to interact with the database.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

# Enforce foreign key constraints and ON DELETE CASCADE on SQLite connections
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if settings.DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """
    FastAPI dependency that provides a database session per request.
    Ensures that the session is always closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def auto_migrate_sqlite():
    """
    Lightweight SQLite schema synchronization helper.
    Ensures newly added columns are present in existing local SQLite databases.
    """
    if not settings.DATABASE_URL.startswith("sqlite"):
        return

    with engine.connect() as conn:
        # Check if skills table exists
        tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='skills'")).fetchall()
        if not tables:
            return

        # Fetch existing columns for skills
        columns_info = conn.execute(text("PRAGMA table_info(skills)")).fetchall()
        existing_cols = {col[1] for col in columns_info}

        new_columns = [
            ("what_is_it", "TEXT"),
            ("why_important", "TEXT"),
            ("where_used", "TEXT"),
            ("benefits", "TEXT"),
            ("challenges", "TEXT"),
            ("prerequisites", "TEXT"),
            ("career_relevance", "TEXT"),
        ]

        for col_name, col_type in new_columns:
            if col_name not in existing_cols:
                conn.execute(text(f"ALTER TABLE skills ADD COLUMN {col_name} {col_type}"))
                conn.commit()

        # Migrate skill_interview_questions
        siq_tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='skill_interview_questions'")).fetchall()
        if siq_tables:
            siq_cols = {c[1] for c in conn.execute(text("PRAGMA table_info(skill_interview_questions)")).fetchall()}
            for col_name in ["simple_syntax", "small_example"]:
                if col_name not in siq_cols:
                    conn.execute(text(f"ALTER TABLE skill_interview_questions ADD COLUMN {col_name} TEXT"))
                    conn.commit()

        # Migrate goal_final_interview_questions
        gfi_tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='goal_final_interview_questions'")).fetchall()
        if gfi_tables:
            gfi_cols = {c[1] for c in conn.execute(text("PRAGMA table_info(goal_final_interview_questions)")).fetchall()}
            for col_name in ["simple_syntax", "small_example"]:
                if col_name not in gfi_cols:
                    conn.execute(text(f"ALTER TABLE goal_final_interview_questions ADD COLUMN {col_name} TEXT"))
                    conn.commit()

        # Migrate user_skill_progress (practical_reviewed, interview_reviewed)
        usp_tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='user_skill_progress'")).fetchall()
        if usp_tables:
            usp_cols = {c[1] for c in conn.execute(text("PRAGMA table_info(user_skill_progress)")).fetchall()}
            for col_name in [("practical_reviewed", "BOOLEAN DEFAULT 0"), ("interview_reviewed", "BOOLEAN DEFAULT 0")]:
                if col_name[0] not in usp_cols:
                    conn.execute(text(f"ALTER TABLE user_skill_progress ADD COLUMN {col_name[0]} {col_name[1]}"))
                    conn.commit()

    # Ensure all tables (including user_certificates) are created
    Base.metadata.create_all(bind=engine)
