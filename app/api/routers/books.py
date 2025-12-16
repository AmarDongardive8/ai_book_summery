from fastapi import APIRouter, Depends,HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.book_schema import BookCreate, BookResponse,BookUpdate
from app.services.book_service import BookService
from app.core.dependencies import require_admin, get_current_user

router = APIRouter()
book_service = BookService()

@router.post("/", response_model=BookResponse,dependencies=[Depends(get_current_user)])
async def create_book(book: BookCreate,db: AsyncSession = Depends(get_db)):
    return await book_service.create_book(db, book)


@router.get("/", response_model=List[BookResponse],dependencies=[Depends(require_admin)])
async def get_books(db: AsyncSession = Depends(get_db)):
    return await book_service.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book: BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await book_service.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await book_service.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


