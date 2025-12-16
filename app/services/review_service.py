from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.model.review import Review

class ReviewService:

    async def add_review(self, db: AsyncSession, book_id: int, user_id: int, data):
        review = Review(
            book_id=book_id,
            user_id=user_id,
            review_text=data.review_text,
            rating=data.rating
        )
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    async def get_reviews_by_book(self, db: AsyncSession, book_id: int):
        result = await db.execute(
            select(Review).where(Review.book_id == book_id)
        )
        return result.scalars().all()

    async def get_book_rating_summary(self, db: AsyncSession, book_id: int):
        result = await db.execute(
            select(
                func.count(Review.id),
                func.avg(Review.rating)
            ).where(Review.book_id == book_id)
        )
        count, avg = result.one()
        return {
            "total_reviews": count or 0,
            "average_rating": round(avg, 2) if avg else None
        }
