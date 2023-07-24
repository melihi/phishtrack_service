import datetime as dt

import sqlalchemy

from ..database.database import Base


class Phish(Base):
    """Database model class .
    Args:
        Base () : declerative base .
    
    """
    __tablename__ = "phishing"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    resource = sqlalchemy.Column(sqlalchemy.String, index=True)
    phish_link = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    date_created = sqlalchemy.Column(sqlalchemy.DateTime, default=dt.datetime.utcnow)
