from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Settings for the application, loaded from environment variables or a .env file.
    """

    data_type_input_path: str = Field(
        validation_alias="DATA_TYPE_JSON_PATH", default="data/data_type.json"
    )
    data_type_dirs_path: str = Field(
        validation_alias="DATA_TYPE_DIRS_JSON_PATH", default="data/data_type_dirs.json"
    )

    class config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()

DATA_TYPE_JSON_PATH = os.path.join(BASE_DIR, Path(settings.data_type_input_path))
DATA_TYPE_DIRS_JSON_PATH = os.path.join(BASE_DIR, Path(settings.data_type_dirs_path))
