from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_CONFIG = {
    "env_file": ".env",
    "env_file_encoding": "utf-8",
    "extra": "ignore",
}


class Configurations(BaseSettings):
    model_config = SettingsConfigDict(**ENV_FILE_CONFIG)

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY: str
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG: bool = False
    ALLOWED_HOSTS: list = ["*"]


configurations = Configurations()


class DatabaseConfigs(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_", **ENV_FILE_CONFIG)

    username: str
    password: str
    dbname: str
    port: str
    host: str


db_configs = DatabaseConfigs()
