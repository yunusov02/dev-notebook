from contextlib import asynccontextmanager

from beyond_crud.books.routes import books_router
from beyond_crud.db.main import init_db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi import status




@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Server is staring")
    
    await init_db()
    yield 
    
    print("Server is shutting down")
    
    
    
    

app = FastAPI(
    title="Beyond CRUD",
    lifespan=lifespan
)

app.include_router(books_router, prefix="/api")



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
