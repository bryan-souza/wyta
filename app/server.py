import os
from pathlib import Path

import nltk
from fastapi import FastAPI

from app.routers import files_router
from app.config import CONFIG

app = FastAPI()


# Events
@app.on_event('startup')
def startup():
    if not CONFIG.storage_path.exists():
        os.mkdir(CONFIG.storage_path)

    if not CONFIG.nltk_path.exists():
        os.mkdir(CONFIG.nltk_path)

    if not Path(CONFIG.nltk_path, 'corpora', 'stopwords').exists():
        nltk.download('stopwords')


# Routers
# TODO: Register routers
app.include_router(files_router)
