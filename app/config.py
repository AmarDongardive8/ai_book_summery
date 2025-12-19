# from pydantic_settings  import BaseSettings
# import os
# from dotenv import load_dotenv
# load_dotenv()

# class Settings(BaseSettings):
#     DATABASE_URL : str = (
#         f"postgresql+asyncpg://"
#         f"{os.getenv('POSTGRES_USER')}:"
#         f"{os.getenv('POSTGRES_PASSWORD')}@"
#         f"{os.getenv('HOST')}:5432/"
#         f"{os.getenv('POSTGRES_DB')}"
#     )

#     model_config  = {
#         "env_file" : ".env",
#         "extra": "allow",
#     }

# settings = Settings()


from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    HOST: str = "db"  # default to Docker service name

    @property
    def DATABASE_URL(self) -> str:
        # URL-encode password if it has special chars
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{quote_plus(self.POSTGRES_PASSWORD)}@{self.HOST}:5432/{self.POSTGRES_DB}"

    model_config = {
        "env_file": ".env",
        "extra": "allow",
    }

settings = Settings()
