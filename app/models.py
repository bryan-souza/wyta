from pydantic import BaseModel
from tinydb import Query

ItemQuery = Query()


class Item(BaseModel):
    digest: str
    filename: str
