from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from homeline.config import settings
from homeline.utils.logging import logger

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    logger.info("Initializing database tables if not existing")
    Base.metadata.create_all(bind=engine)
    
    # If using an in-memory database or as a demo, seed the DB
    if settings.DATABASE_URL == "sqlite:///:memory:" or ":memory:" in settings.DATABASE_URL:
        from homeline.db.seed_data import seed_database
        db = SessionLocal()
        try:
            seed_database(db)
            logger.info("Demo database seeded successfully")
        finally:
            db.close()
