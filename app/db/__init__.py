from __future__ import annotations


def init_db() -> None:
    from app.db.base import Base  # Imported lazily to avoid circular imports
    from app.db.session import engine
    from app.db.seed import run_initial_seed

    Base.metadata.create_all(bind=engine)
    run_initial_seed()

