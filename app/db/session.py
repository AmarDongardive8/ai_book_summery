from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

Base = declarative_base()
# SQLALCHEMY_DB_URL = "sqlite+aiosqlite:///./sql_app.db"
# engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
if not settings.DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required")

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
