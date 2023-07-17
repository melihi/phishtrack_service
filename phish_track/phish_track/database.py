import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from dynaconf import Dynaconf

secrets = Dynaconf(settings_files=["settings.toml",'.secrets.toml'])
host = secrets.host
username = secrets.postgre_user
password = secrets.postgre_password


DATABASE_URL = "postgresql://"+username+":"+password+"@"+host+"/phishtrack_db"

engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()



