import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.review_service import ReviewService
from app.services.book_service import BookService
from app.services.recommendation_service import RecommendationService
from app.schemas.review_schema import ReviewCreate
from app.schemas.recommendation_schema import PreferenceRequest
from app.model.review import Review

@pytest.mark.asyncio
async def test_add_review_positive():
    db_mock = AsyncMock()
    db_mock.add = MagicMock()
    db_mock.commit = AsyncMock()
    db_mock.refresh = AsyncMock()

    review_data = ReviewCreate(rating=5, review_text="Great book!")
    user_id = 1
    book_id = 1

    service = ReviewService()

    result = await service.add_review(db_mock, book_id, user_id, review_data)

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()
    assert isinstance(result, Review)
    assert result.review_text == "Great book!"
    assert result.rating == 5

@pytest.mark.asyncio
async def test_get_reviews_by_book_positive():
    db_mock = AsyncMock()
    reviews = [
        Review(id=1, book_id=1, user_id=1, rating=5, review_text="Good"),
        Review(id=2, book_id=1, user_id=2, rating=4, review_text="Nice")
    ]
    result_mock = MagicMock()

    scalars_mock = MagicMock()
    scalars_mock.all.return_value = reviews
    result_mock.scalars.return_value = scalars_mock
    db_mock.execute.return_value = result_mock
    service = ReviewService()
    result = await service.get_reviews_by_book(db_mock, 1)

    assert result == reviews

@pytest.mark.asyncio
async def test_get_book_rating_summary_positive():
    db_mock = AsyncMock()
    rating_summary = {"average_rating": 4.5, "total_reviews": 2}
    service = ReviewService()
    service.get_book_rating_summary = AsyncMock(return_value=rating_summary)

    result = await service.get_book_rating_summary(db_mock, 1)
    assert result["average_rating"] == 4.5
    assert result["total_reviews"] == 2

@pytest.mark.asyncio
async def test_get_recommendations_positive():
    db_mock = AsyncMock()
    service = RecommendationService()

    preference = "Programming"
    service.recommend_books = AsyncMock(return_value=[
        {"id": 1, "title": "Clean Code", "genre": "Programming"},
        {"id": 2, "title": "The Pragmatic Programmer", "genre": "Programming"}
    ])

    result = await service.recommend_books(db_mock, preference)
    assert len(result) == 2
    assert result[0]["genre"] == "Programming"
    service.recommend_books.assert_called_once_with(db_mock, preference)
