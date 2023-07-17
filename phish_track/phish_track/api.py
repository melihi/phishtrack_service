import uvicorn
import fastapi as _fastapi

import database as _database
import models as _models
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()


@app.post("/api/phish/", response_model=_schemas.Phish)
async def create_phish(
    phish: _schemas.CreatePhish, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    
    return await _services.create_phish(phish=phish, db=db)


@app.get("/api/phishs/", response_model=List[_schemas.Phish])
async def get_phishs(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_phishs(db=db)


@app.get("/api/phishs/{phish_id}", response_model=_schemas.Phish)
async def get_phish(
    phish_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    phish = await _services.get_phish(phish_id=phish_id, db=db)
    if phish is None:
        raise _fastapi.HTTPException(status_code=404, detail="Phish does not exist")
    return phish


@app.delete("/api/phishs/{phish_id}")
async def delete_phish(phish_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    phish = await _services.get_phish(db=db,phish_id=phish_id)
    if phish is None:
        raise _fastapi.HTTPException(status_code=404,detail="Phish does not exist")
    await _services.delete_phish(phish,db=db) 
    return "Successfull deleted"
            
@app.put("/api/phishs/{phish_id}",response_model=_schemas.Phish)
async def update_phish(phish_id: int,phish_data:_schemas.CreatePhish ,db: _orm.Session = _fastapi.Depends(_services.get_db)):
    phish = await _services.get_phish(db=db,phish_id=phish_id)
    if phish is None:
        raise _fastapi.HTTPException(status_code=404,detail="Phish does not exist")
    
    return await _services.update_phish(phish_data=phish_data,phish=phish,db=db)

@app.get("/")
async def root():
    return {"message": "Welcome To PhishTrack Fastapi"}


def start():
    """Launched with `poetry run start` at root level"""

    uvicorn.run(
        "phishtrack.api:app", host="127.0.0.1", port=8000, reload=True, workers=2
    )
