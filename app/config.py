from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    # Path configurations
    app_path = Path(__file__).parent.absolute()
    root_path = Path(app_path).parent.absolute()
    storage_path = Path(root_path, 'data').absolute()


CONFIG = Settings()
