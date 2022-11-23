from pathlib import Path

from tinydb import TinyDB

from app.config import CONFIG
from app.exceptions import ItemNotFoundError
from app.models import Item, ItemQuery


class StorageController:

    @staticmethod
    def write(content: bytes, filename: str):
        filepath = Path(CONFIG.storage_path, filename)
        with open(filepath, 'w+b') as _file:
            _file.write(content)


class ItemController:

    def __init__(self):
        self._db = TinyDB(f'{CONFIG.root_path}/db.json')

    def get_by_digest(self, digest: str):
        result = self._db.get(ItemQuery.digest == digest)
        if result is None:
            raise ItemNotFoundError()

        return Item(**result)

    def insert(self, item: Item):
        self._db.insert(dict(item))
        return item
