from typing import List
import fastapi
from ..database.database import *
from ..schemas.schemas import *
from ..services.services import get_all_phishs
from sqlalchemy.orm import Session
 
# initialize Fastapi
app = fastapi.FastAPI()

# create table in postgresql
add_tables()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/phishs/", response_model=List[Phish])
def get_phishs(skip: int = 0, limit: int = 100, db: Session = fastapi.Depends(get_db)):
    phishs = get_all_phishs(db, skip=skip, limit=limit)
    return phishs



@app.get("/")
async def root():
    return {"message": "Welcome To PhishTrack Fastapi"}
