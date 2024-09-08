from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

# BOOK CLASS
class Book:
    id: int
    title: str
    author: str
    pages: int
    category: str

    def __init__(self, id, title, author, pages, category):
        self.id = id
        self.title = title
        self.author = author
        self.pages = pages
        self.category = category

# for validation
class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    category: str



BOOKS = [
    Book(1, "Murder in the Nile", "Agatha Christie", 200, "mistery"),
    Book(2, "Murder in the Orient Express", "Agatha Christie", 200, "mistery"),
    Book(3, "The Dark Forest", "Liu Cixin", 750, "scifi"),
    Book(4, "The Three Body Problem", "Liu Cixin", 600, "scifi"),
    Book(5, "Pet Cemetery", "Stephen King", 500, "horror"),
    Book(6, "The Shining", "Stephen King", 666, "horror"),
    Book(7, "Dune", "Frank Herbert", 600, "scifi"),
    Book(8, "The Thursday Murder Club", "Richard Osman", 350, "mistery"),
]

# - - - - - - -

@app.get("/books")
def index():
    return BOOKS


@app.get("/books/{book_id}")
def show(book_id: int):
    return next((book for book in BOOKS if book.id == book_id), None)

@app.post("/books/create-book")
def create(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
