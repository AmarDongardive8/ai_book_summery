from sqlalchemy.ext.asyncio import AsyncSession
from app.model.book import Book
from app.services.llm_service import LLMService
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class BookService:
    def __init__(self):
        self.llm_service = LLMService()

    async def create_book(self, db: AsyncSession, data):
        try:
            
            summary = await self.llm_service.generate_summary(
                title=data.title,
                author=data.author,
                content=data.content
            )

            book = Book(
                title=data.title,
                author=data.author,
                genre=data.genre,
                year_published=data.year_published,
                summary=summary
            )

            await db.add(book)
            await db.commit()
            await db.refresh(book)
            return book
        except SQLAlchemyError as db_err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred while creating book"
            ) from db_err

        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create book"
            ) from err
    
    async def get_all_books(self, db):
        try:
            result = await db.execute(select(Book))
            return result.scalars().all()
        except SQLAlchemyError as db_err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch books"
            ) from db_err

    async def get_book_by_id(self, db, book_id: int):
        try:
            result = await db.execute(
                select(Book).where(Book.id == book_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as db_err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch book"
            ) from db_err
    

    async def update_book(self, db, book_id: int, data):
        try:
            book = await self.get_book_by_id(db, book_id)
            if not book:
                return None

            # for field, value in data.dict(exclude_unset=True).items():
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(book, field, value)

            await db.commit()
            await db.refresh(book)
            return book
        except SQLAlchemyError as db_err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update book"
            ) from db_err

    async def delete_book(self, db, book_id: int):
        try:
            book = await self.get_book_by_id(db, book_id)
            if not book:
                return False

            await db.delete(book)
            await db.commit()
            return True
        except SQLAlchemyError as db_err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete book"
            ) from db_err
