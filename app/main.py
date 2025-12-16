from fastapi import FastAPI
from app.api.routers import books,auth,reviews
from app.db.session import engine
from app.db.session import Base

app = FastAPI(title="AI Book Management System")

# @app.on_event("startup")
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


app.include_router(auth.router)
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])


