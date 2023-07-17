import datetime as _dt
import sqlalchemy as _sql
import database as _database


class Phish(_database.Base):
    __tablename__ = "phishing"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    resource = _sql.Column(_sql.String, index=True)
    phish_link = _sql.Column(_sql.String, index=True, unique=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
