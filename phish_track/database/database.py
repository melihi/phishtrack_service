from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import *

host = settings.host
username = settings.postgre_user
password = settings.postgre_password


DATABASE_URL = (
    "postgresql://" + username + ":" + password + "@" + host + "/phishtrack_db"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def add_tables():
    """
    Creates database tables .
    """
    return Base.metadata.create_all(bind=engine)



