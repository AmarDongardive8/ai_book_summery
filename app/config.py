from pydantic_settings  import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL : str = (
        f"postgresql+asyncpg://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('HOST')}:5432/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    class Config:
        env_file = ".env"

settings = Settings()
