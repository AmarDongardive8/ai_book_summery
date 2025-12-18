from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
<<<<<<< HEAD


# SQLALCHEMY_DB_URL =  "sqlite:///./sql_app.db"
SQLALCHEMY_DB_URL = "sqlite+aiosqlite:///./sql_app.db"
=======
import os


# SQLALCHEMY_DB_URL =  "sqlite:///./sql_app.db"
# SQLALCHEMY_DB_URL = "sqlite+aiosqlite:///./sql_app.db"

DATABASE_URL = f"postgres+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"

>>>>>>> bf6d81f65e764bc51eda2a5ecaf880e821b80f96



Base = declarative_base()

# engine = create_async_engine(settings.DATABASE_URL, echo=True)
<<<<<<< HEAD
engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
=======
# engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
engine = create_async_engine(DATABASE_URL, echo=True)

>>>>>>> bf6d81f65e764bc51eda2a5ecaf880e821b80f96


AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
