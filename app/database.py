from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)


Base = declarative_base()

