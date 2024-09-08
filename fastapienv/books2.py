from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

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
    id: Optional[int] = Field(description="ID is not required on Create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    pages: int = Field(gt=0)
    category: str

    model_config = {
	"json_schema_extra": {
		"example": {
			"title": "New book", 
			"author": "new author", 
			"pages": 100, 
			"category": "new category", 
		}
	}
}



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
    new_book.id = increase_book_id()
    BOOKS.append(new_book)

# - - - 関数
def increase_book_id():
    return BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
