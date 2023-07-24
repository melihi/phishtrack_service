import datetime as dt

from pydantic import BaseModel


class BasePhish(BaseModel):
    resource: str
    phish_link: str


class Phish(BasePhish):
    id: int
    date_created: dt.datetime

    class Config:
        # orm_mode = True
        from_attributes = True
