from sqlalchemy.orm import Session
from typing import Generator
from homeline.db.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """Dependency to provide a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
