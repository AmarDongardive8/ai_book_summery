# from pydantic_settings  import BaseSettings
# import os
# from dotenv import load_dotenv
# load_dotenv()

# class Settings(BaseSettings):
#     SECRET_KEY : str
#     OPENAI_MODEL : str
#     OPENAI_MAX_TOKENS : int
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
# # 👇 PRINT HERE (for testing only)
# print("SECRET_KEY =", settings.SECRET_KEY)


from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    DATABASE_TYPE : str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    HOST: str 
    PORT : str
    
    SECRET_KEY : str
    OPENAI_MODEL : str
    OPENAI_MAX_TOKENS : int

    @property
    def DATABASE_URL(self) -> str:
        # URL-encode password if it has special chars
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{quote_plus(self.POSTGRES_PASSWORD)}@{self.HOST}:{self.PORT}/{self.POSTGRES_DB}"

    model_config = {
        "env_file": ".env",
        "extra": "allow",
    }

settings = Settings()
