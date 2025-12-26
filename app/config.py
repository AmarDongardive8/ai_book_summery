from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    HOST: str 
    PORT : str
    
    SECRET_KEY : str
    OPENAI_MODEL : str
    OPENAI_MAX_TOKEN : int

    @property
    def DATABASE_URL(self) -> str:
        # URL-encode password if it has special chars
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{quote_plus(self.POSTGRES_PASSWORD)}@{self.HOST}:{self.PORT}/{self.POSTGRES_DB}"

    model_config = {
        "env_file": ".env",
        "extra": "allow",
    }

settings = Settings()
