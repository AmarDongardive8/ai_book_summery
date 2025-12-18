from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os



# SQLALCHEMY_DB_URL =  "sqlite:///./sql_app.db"
# SQLALCHEMY_DB_URL = "sqlite+aiosqlite:///./sql_app.db"

# DATABASE_URL = f"postgres+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"db:5432/"
    f"{os.getenv('POSTGRES_DB')}"
)


Base = declarative_base()

# engine = create_async_engine(settings.DATABASE_URL, echo=True)
# engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
engine = create_async_engine(DATABASE_URL, echo=True)



AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
