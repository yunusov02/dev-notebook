from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi import status

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


books: List[Book] = []

@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    books.append(book)
    return book


@app.patch("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update: BookUpdateModel):
    for book in books:
        if book.id == book_id:
            book.title = book_update.title
            book.author = book_update.author
            book.publisher = book_update.publisher
            book.page_count = book_update.page_count
            book.language = book_update.language
            return book

    HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    
    HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")




@app.get("/")
async def read_root():
    return {"message": "Welcome to Beyond CRUD!"}


"""
User Agent: This string allows network protocol peers to identify the application
            responsible for the request, the operating system.
            
            User-Agent an HTTP request header that tells the server which clients is making the request and some information about that client


Host:       The speicific the domain name of the server and the TCP port number on which server is listening it
            Header tells the servet which host the client wants to communicate with
            Example:    api.exampl.com

Accept:     applicaiton/json

Accept-Language:    en-US




    GET /api/products HTTP/1.1
    Host: api.example.com
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64)
    Accept: application/json
    Accept-Language: en-US,en;q=0.9,ru;q=0.8
    Accept-Encoding: gzip, br
    Referer: https://shop.example.com/
    Connection: keep-alive

"""
