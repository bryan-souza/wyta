import re
from pathlib import Path
from tinydb import TinyDB
from collections import Counter

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


class ReportController:

    def __init__(self):
        self._words = []
        self._users = []

    def create_report(self, digests):
        normal_pattern = r'([0-9]{2}\/[0-9]{2}/[0-9]{4}\ [0-9]+:[0-9]{2}.+)\ -\ (.*?):\ (.+)'

        for _digest in digests:
            filepath = Path(CONFIG.storage_path, _digest)
            with open(filepath, 'r', encoding='utf-8') as _file:
                for _line in _file.readlines():
                    match = re.match(normal_pattern, _line)
                    if match is None:
                        continue

                    _, user, message = match.group(1, 2, 3)

                    if user not in self._users:
                        self._users.append(user)

                    self._words.extend(message.split())

        counter = Counter(self._words)

        return {
            'users': self._users,
            'top_words': counter.most_common(10)
        }