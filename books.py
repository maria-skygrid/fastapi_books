from fastapi import FastAPI, Body
import books_data as books

app = FastAPI()
books = books.BOOKS

@app.get("/")
def first_api():
    return { "message": "Hello world" }

@app.get("/books")
def get_books():
    return books


# path parameters
@app.get("/books/{book_id}")
def show(book_id: int):
    for book in books:
        return book.get('id') == book_id and book


# query parameters
@app.get("/books/")
def books_by_category(category: str):
    books_list = []
    for book in books:
        if book.get("category") == category:
            books_list.append(book)
    return books_list

# query and path parameters together
@app.get("/books/{book_author}/")
def read_author_category_by_query(book_author: str, category: str):
    books_list = []
    for book in books:
        if (book.get("author").casefold() == book_author and
                book.get("category").casefold() == category):
            books_list.append(book)
    return books_list


# -- POST --
@app.post("/books/create_book")
def create(new_book=Body()):
    books.append(new_book)
    return f"Book {new_book.get("title")} added"


# -- PUT --
@app.put("/books/update_book")
def update(updated_book=Body()):
    for index, book in enumerate(books):
        if book.get("id") == updated_book.get("id"):
            books[index] = updated_book
    return f"Book {updated_book.get("title")} updated"


# -- DELETE --
@app.delete("/books/delete_book/{book_id}")
def delete(book_id: int):
    for i in range(len(books)):
        if books[i].get("id") == book_id:
            books.pop(i)
            break
    return f"Book with id {book_id} deleted"


# -- INDEX BOOKS BY AUTHOR
@app.get("/books/author/{book_author}")
def index_filter_by_book_author(book_author: str):
    book_list = []
    for book in books:
        if book.get("author").casefold() == book_author.casefold():
            book_list.append(book)
    return book_list
