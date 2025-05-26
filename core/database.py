import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/mental_padi"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This function is used to create the database tables
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()