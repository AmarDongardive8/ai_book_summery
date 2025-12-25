from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.model.review import Review
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class ReviewService:

    async def add_review(self, db: AsyncSession, book_id: int, user_id: int, data):
        try:
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
        except SQLAlchemyError as db_err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add review"
            ) from db_err
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while adding review"
            ) from err

    async def get_reviews_by_book(self, db: AsyncSession, book_id: int):
        try:
            result = await db.execute(
                select(Review).where(Review.book_id == book_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as db_err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch reviews"
            ) from db_err
            

    async def get_book_rating_summary(self, db: AsyncSession, book_id: int):
        try:
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
        except SQLAlchemyError as db_err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to calculate rating summary"
            ) from db_err
