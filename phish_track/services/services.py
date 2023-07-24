from sqlalchemy.orm import Session
from typing import List
from ..models.models import Phish
from ..schemas.schemas import BasePhish as schema


"""
async def get_all_phishs(db: "Session") -> List[schema.Phish]:
    phishs = db.query(models.Phish).all()
    return list(map(schema.Phish.from_orm, phishs))


"""


def get_all_phishs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Phish).offset(skip).limit(limit).all()


""" def remove_all_phishs(db: Session):
    db.query(Phish).delete()
    db.commit
    
 """
