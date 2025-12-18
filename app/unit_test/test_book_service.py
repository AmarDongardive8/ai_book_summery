import pytest
from unittest.mock import AsyncMock,MagicMock
from app.services.book_service import BookService
from app.schemas.book_schema import BookCreate , BookUpdate
from app.model.book import Book

@pytest.mark.asyncio
async def test_create_book_with_llm_summary():
    
    db_mock = AsyncMock()

    book_data = BookCreate(
        title="Clean Code",
        author="Robert C. Martin",
        genre="Programming",
        year_published=2008,
        content="This book teaches clean coding practices"
    )

    service = BookService()

    service.llm_service.generate_summary = AsyncMock(
        return_value="Clean Code: A guide to writing clean and maintainable code"
    )

    result = await service.create_book(db_mock, book_data)

    service.llm_service.generate_summary.assert_called_once_with(
        title=book_data.title,
        author=book_data.author,
        content=book_data.content
    )

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

    # 8️⃣ Assertions: Result
    assert isinstance(result, Book)
    assert result.summary.startswith("Clean Code")
    assert result.title == "Clean Code"


@pytest.mark.asyncio
async def test_get_book_by_id_positive():
    db_mock = AsyncMock()
    book = Book(id=1, title="Book1", author="Author1", genre="G1", year_published=2020, summary="S1")
    # db_mock.execute.return_value.scalar_one_or_none = AsyncMock(return_value=book)

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = book

    db_mock.execute.return_value = result_mock
    service = BookService()
    result = await service.get_book_by_id(db_mock, 1)
    assert result == book

@pytest.mark.asyncio
async def test_get_book_by_id_negative():
    db_mock = AsyncMock()
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None

    db_mock.execute.return_value = result_mock
    
    service = BookService()
    result = await service.get_book_by_id(db_mock, 999)
    assert result is None

@pytest.mark.asyncio
async def test_get_all_books_positive():
    db_mock = AsyncMock()
    books = [
        Book(id=1, title="Book1", author="A1", genre="G1", year_published=2020, summary="S1"),
        Book(id=2, title="Book2", author="A2", genre="G2", year_published=2021, summary="S2")
    ]

    result_mock = MagicMock()

    scalars_mock = MagicMock()
    scalars_mock.all.return_value = books

    result_mock.scalars.return_value = scalars_mock
    db_mock.execute.return_value = result_mock

    service = BookService()
    result = await service.get_all_books(db_mock)
    assert result == books


@pytest.mark.asyncio
async def test_update_book_positive():
    db_mock = AsyncMock()
    book = Book(id=1, title="Old", author="Author", genre="G1", year_published=2020, summary="Old summary")
    
    update_data = BookUpdate(title="Updated", author="Author", genre="G1", year_published=2020, content="New content")
    service = BookService()
    service.get_book_by_id = AsyncMock(return_value=book)

    result = await service.update_book(db_mock, 1, update_data)
    assert result.title == "Updated"
    assert result.author == "Author"
    assert result.year_published == 2020


@pytest.mark.asyncio
async def test_update_book_negative():
    db_mock = AsyncMock()
    update_data = BookUpdate(title="Updated", author="Author", genre="G1", year_published=2020, content="New content")

    service = BookService()
    service.get_book_by_id = AsyncMock(return_value=None)
    result = await service.update_book(db_mock, 999, update_data)
    assert result is None


@pytest.mark.asyncio
async def test_delete_book_positive():
    db_mock = AsyncMock()
    book = Book(id=1, title="Book1", author="Author", genre="G1", year_published=2020, summary="S1")

    service = BookService()
    service.get_book_by_id = AsyncMock(return_value=book)

    db_mock.delete = AsyncMock()
    db_mock.commit = AsyncMock()
    result = await service.delete_book(db_mock, 1)
    assert result is True
    db_mock.delete.assert_called_once()
    db_mock.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_book_negative():
    db_mock = AsyncMock()

    service = BookService()
    service.get_book_by_id = AsyncMock(return_value=None)

    result = await service.delete_book(db_mock, 999)
    assert result is False