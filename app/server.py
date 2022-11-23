from fastapi import FastAPI

from app.routers import files_router

app = FastAPI()


# TODO: Register routers
app.include_router(files_router)
