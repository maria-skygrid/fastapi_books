from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

# BOOK CLASS
class Book:
    id: int
    title: str
    author: str
    rating: float
    pages: int
    category: str
    published_year: int

    def __init__(self, id, title, author, rating, pages, category, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating
        self.pages = pages
        self.category = category
        self.published_year = published_year

# for validation
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not required on Create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    rating: float = Field(gt=-1, le=5)
    pages: int = Field(gt=0)
    category: str
    published_year: int

    model_config = {
	"json_schema_extra": {
		"example": {
			"title": "New book", 
			"author": "new author", 
            "rating": 3.5,
			"pages": 100, 
			"category": "new category", 
            "published_year": 2020,
		}
	}
}



BOOKS = [
    Book(id=1, title="Murder in the Nile", author="Agatha Christie", rating=3, pages=200, category="mistery", published_year=1980),
    Book(id=2, title="Murder in the Orient Express", author="Agatha Christie", rating=4, pages=200, category="mistery", published_year=1986),
    Book(id=3, title="The Dark Forest", author="Liu Cixin", rating=4.5, pages=750, category="scifi", published_year=2016),
    Book(id=4, title="The Three Body Problem", author="Liu Cixin", rating=3, pages=600, category="scifi", published_year=2014),
    Book(id=5, title="Pet Cemetery", author="Stephen King", rating=5, pages=500, category="horror", published_year=2002),
    Book(id=6, title="The Shining", author="Stephen King", rating=3, pages=666, category="horror", published_year=1999),
    Book(id=7, title="Dune", author="Frank Herbert", rating=3.5, pages=600, category="scifi", published_year=1976),
    Book(id=8, title="The Thursday Murder Club", author="Richard Osman", rating=4.5, pages=350, category="mistery", published_year=2020),
]

# - - - - - - -

# - - - INDEX
@app.get("/books", status_code=status.HTTP_200_OK)
def index():
    return BOOKS

# - - - SHOW
@app.get("/books/{book_id}")
def show(book_id: int = Path(gt=0)):
    book = next((book for book in BOOKS if book.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail='Item not found')
    return book    

# - - - BOOKS BY RATING
@app.get("/books/by-rating/")
def book_by_rating(book_rating: float = Query(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating == book_rating ]

# - - - BOOKS BY PUBLISHED YEAR
@app.get("/books/by-published-year/")
def books_by_published_year(published_year: int):
    return [book for book in BOOKS if book.published_year == published_year]

# - - - CREATE
@app.post("/books/create-book", status_code=status.HTTP_201_CREATED)
def create(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book.id = increase_book_id()
    BOOKS.append(new_book)

# - - - UPDATE
@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
def update(book_request: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request

# - - - DELETE
@app.delete("/books/delete-book", status_code=status.HTTP_204_NO_CONTENT)
def delete(book_id: int = Path(gt=0)):
   global BOOKS
   BOOKS = [book for book in BOOKS if book.id != book_id]

# - - - 関数
def increase_book_id():
    return BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
