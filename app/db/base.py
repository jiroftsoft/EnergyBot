from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Ensure models are imported so metadata is populated
from app.db import models  # noqa: E402,F401

