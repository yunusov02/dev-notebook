
from typing import List
import uuid

from beyond_crud.auth.dependencies import AccessTokenBearer, RoleChecker
from beyond_crud.books.service import BookService
from beyond_crud.db.main import get_session

from .schemas import Book, BookCreateModel, BookUpdateModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


books_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@books_router.get("/books", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
):

    books = await book_service.get_all_books(session)
    return books



@books_router.get("/books/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
):

    book = await book_service.get_book(book_uid, session)

    if book:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@books_router.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
):

    book = await book_service.create_book(book_data, session)

    return book


@books_router.patch("/books/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def update_book(
    book_uid: uuid.UUID,
    book_update: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
):

    book = await book_service.update_book(book_uid, book_update, session)

    if book:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@books_router.delete("/books/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
):

    deleted = await book_service.delete_book(book_uid, session)

    if deleted:
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
