from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# SQLALCHEMY_DB_URL =  "sqlite:///./sql_app.db"
SQLALCHEMY_DB_URL = "sqlite+aiosqlite:///./sql_app.db"



Base = declarative_base()

# engine = create_async_engine(settings.DATABASE_URL, echo=True)
engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
