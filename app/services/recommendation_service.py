from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model.book import Book
from app.services.llm_service import LLMRecomndationService
from sqlalchemy import select, or_

class RecommendationService:
    def __init__(self):
        self.llm_service = LLMRecomndationService()

    async def recommend_books(self,db: AsyncSession,preference: str):
        result = await db.execute(select(Book.genre).distinct())
        all_genres_str =(",").join(result.scalars().all())
        print("result:------",all_genres_str)
        genre = await self.llm_service.extract_genre(preference,all_genres_str)
        genres = [g.strip() for g in genre.split(",")]
        query = select(Book).where(
            or_(*[Book.genre.ilike(f"%{g}%") for g in genres])
        ).limit(10)
        result = await db.execute(query)
        books = result.scalars().all()

        return {
            "detected_genre": genre,
            "books": books
        }
