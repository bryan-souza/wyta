import os
import nltk
from pathlib import Path
from fastapi import FastAPI
from fastapi.middlewares.cors import CORSMiddleware

from app.routers import files_router
from app.config import CONFIG

app = FastAPI()


# Middlewares

cors_allowed_origins = ['http://localhost:5173', 'http://127.0.0.1:5173']
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


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
