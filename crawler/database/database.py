import datetime as dt

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import insert
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


class Phish(Base):
    """
    Phishing database model .
    Args:
        Base (_DeclarativeBase) : 
    """

    __tablename__ = "phishing"
    id = Column(Integer, primary_key=True, index=True)
    resource = Column(String, index=True)
    phish_link = Column(String, index=True, unique=True)
    date_created = Column(DateTime, default=dt.datetime.utcnow)


def bulk_insert_users(phish_data: tuple) -> None:
    """
    Bulk insert to database .
    Args:
       phish_data: tuple
    """
    with SessionLocal() as session:
        # session.bulk_insert_mappings(Phish, users_data)
        stmt = insert(Phish).values(phish_data)
        on_conflict_stmt = stmt.on_conflict_do_update(
            # if phish link exists
            index_elements=["phish_link"],
            # if phish_link exists , update date_created
            set_={
                # "resource": stmt.excluded.resource,
                # "phish_link": stmt.excluded.phish_link,
                "date_created": stmt.excluded.date_created,
            },
        )
        session.execute(on_conflict_stmt)
        session.commit()
