from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.review_schema import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService
from app.core.dependencies import get_current_user
from app.services.book_service import  BookService
from app.core.dependencies import require_admin, get_current_user
from app.schemas.recommendation_schema import PreferenceRequest
from app.services.recommendation_service import RecommendationService

service = RecommendationService()

router = APIRouter()
review_service = ReviewService()
book_service=BookService()

@router.post("/create_reviews/{book_id}", response_model=ReviewResponse,dependencies=[Depends(get_current_user)])
async def add_review(book_id: int,review: ReviewCreate,db: AsyncSession = Depends(get_db),user = Depends(get_current_user)):
    return await review_service.add_review(db, book_id, user.id, review)

@router.get("/get_reviews/{book_id}", response_model=List[ReviewResponse],dependencies=[Depends(get_current_user)])
async def get_reviews(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await review_service.get_reviews_by_book(db, book_id)


@router.get("/get_summary/{book_id}",dependencies=[Depends(get_current_user)])
async def book_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    rating_data = await review_service.get_book_rating_summary(db, book_id)

    return {
        "book_id": book.id,
        "title": book.title,
        "summary": book.summary,
        "ratings": rating_data
    }

@router.post("/recommendations")
async def get_recommendations(data: PreferenceRequest,db: AsyncSession = Depends(get_db)):
    return await service.recommend_books(db, data.preference)