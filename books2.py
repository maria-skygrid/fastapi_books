from fastapi import FastAPI, Body

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


@app.post("/books/{book_id}")
def show(book_id: int):
    return next((book for book in BOOKS if book.get(id) == book_id), None)

@app.put("/books/create_book")
def create(new_book=Body()):
    books.append(new_book)

# @app.put("/books/update_book")
# def update(updated_book=Body()):
#     for index in books:
