import database as _database
import models as _models
import schemas as _schemas
from typing import TYPE_CHECKING, List
import logging as _logging
from sqlalchemy import exc

#_logging.basicConfig(level=_logging.INFO)

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

_add_tables()
def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_phish(phish: _schemas.CreatePhish, db: "Session") -> _schemas.Phish:
    try:
        phish = _models.Phish(**phish.dict())
        db.add(phish)
        db.commit()
        db.refresh(phish)
         
    except exc.OperationalError as e:
        print("Hata : operational error")
    except exc.IntegrityError as e:
        print("Hata: Integrity")
     
    
    return _schemas.Phish.from_orm(phish)


async def get_all_phishs(db: "Session") -> List[_schemas.Phish]:
    phishs = db.query(_models.Phish).all()
    return list(map(_schemas.Phish.from_orm, phishs))


async def get_phish(phish_id: int, db: "Session"):
    phish = db.query(_models.Phish).filter(_models.Phish.id == phish_id).first()
    return phish


async def delete_phish(phish: _models.Phish, db: "Session"):
    db.delete(phish)
    db.commit()


async def update_phish(
    phish_data: _schemas.CreatePhish, phish: _models.Phish, db: "Session"
) -> _schemas.Phish:
    phish.phish_link = phish_data.phish_link
    phish.resource = phish_data.resource
    db.commit()
    db.refresh(phish)
    return _schemas.Phish.from_orm(phish)
