from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import redis

# DATABASE_URL = os.getenv("postgresql://postgres:Pass123@localhost/workflows_db", "postgresql://user:password@localhost/workflows_db")

DATABASE_URL = "postgresql://postgres:Pass123@localhost/workflows_db"

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            cls._instance.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine))
        return cls._instance

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_instance = Database()
Base = declarative_base()

# Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)