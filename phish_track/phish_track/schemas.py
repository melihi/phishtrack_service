import datetime as _dt
import pydantic as _pydantic


class _BasePhish(_pydantic.BaseModel):
    resource: str
    phish_link: str


class Phish(_BasePhish):
    id: int
    date_created: _dt.datetime

    class Config:
        from_attributes = True


class CreatePhish(_BasePhish):
    pass
