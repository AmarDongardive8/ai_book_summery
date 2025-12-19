from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

Base = declarative_base()

# engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
engine = create_async_engine(settings.DATABASE_URL, echo=True)



AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
