import re
import string
from pathlib import Path
from tinydb import TinyDB
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

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
        media_pattern = r'.*<.+>.*'
        normal_pattern = r'([0-9]{2}\/[0-9]{2}/[0-9]{4}\ [0-9]+:[0-9]{2}.+)\ -\ (.*?):\ (.+)'
        _stopwords = [*stopwords.words('portuguese'), *string.punctuation]

        for _digest in digests:
            filepath = Path(CONFIG.storage_path, _digest)
            with open(filepath, 'r', encoding='utf-8') as _file:
                for _line in _file.readlines():
                    # Check for medias, ignore if present
                    match = re.match(media_pattern, _line)
                    if match is not None:
                        continue

                    # Check for valid messages
                    match = re.match(normal_pattern, _line)
                    if match is None:
                        continue

                    _, user, message = match.group(1, 2, 3)

                    if user not in self._users:
                        self._users.append(user)

                    self._words.extend(message.split())

        # Convert to lowercase
        self._words = [w.lower() for w in self._words]

        # Fix some slangs
        for i, word in enumerate(self._words):
            if word == 'n':
                self._words[i] = 'não'

            if word == 'q':
                self._words[i] = 'que'

            if word == 'pq':
                self._words[i] = 'por'
                self._words[i + 1] = 'que'

            if word == 'pra':
                self._words[i] = 'para'

        # Remove stopwords
        valid_words = []
        for word in self._words:
            if word not in _stopwords:
                valid_words.append(word)

        # Do some counting
        counter = Counter(valid_words)
        top_words = [{'word': x[0], 'count': x[1]} for x in counter.most_common(10)]

        return {
            'users': self._users,
            'top_words': top_words
        }
