from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base, Session

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/archreq_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind = engine   

)
Base = declarative_base()


#---------------------------
# DB Dependency
#---------------------------

def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
