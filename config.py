from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class AppValues:
    TITLE_APP = "OFApp"
    WIDTH_APP = 800
    HEIGHT_APP = 800


class Settings(BaseSettings):
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""
    OF_API_KEY: str = ""
    OF_API_BASE_URL: str = ""

    @property
    def database_url_asyncpg(self):
        return os.getenv(
            "DATABASE_URL",
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
        )

    @property
    def database_url_psycopg(self):
        return os.getenv(
            "DATABASE_URL",
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
