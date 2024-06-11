# from fastapi import FastAPI

# app = FastAPI()

# book_data = [
#     {
#         "name":"computer lang",
#         "author":"ritu",
#         "year":"2020",
#         "genre":"tech",
#         "price":"250",
#         "item_in_stock":"500"
#     },
# ]

# class Book:
#     name=None
#     author_name = None
#     price=None
#     stock = None
#     publish_year = None


# @app.get("/")
# def get_book_data():
#     return {"data":book_data}


# @app.post("/add_book",response_model=Book)
# def add_book(Book:Book):
#     return {"msg":"book added successfully"}



import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware




# Define the Pydantic model
class BookCreate(BaseModel):
    name: str
    author_name: str
    price: float
    stock: int
    publish_year: int
    
class User(BaseModel):
    name: str
    email: str
    phone_no: str
    password: str
    is_admin: bool




# Initialize the FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Database connection and initialization
DATABASE_PATH = "./test.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        author_name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        publish_year INTEGER NOT NULL
    )          
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone_no INTEGER NOT NULL,
            password TEXT NOT NULL,
            is_admin TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def get_All_book():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY id DESC')
    book = cursor.fetchall()
    all_book = []
    for item in book:
        all_book.append(item)

    conn.close()
    if book is None:
        raise HTTPException(status_code=404, detail="No book in the database")
    return {"data":all_book}

@app.get("/limit/{limit}")
def get_limited_book(limit:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    q = f"SELECT * FROM books ORDER BY id DESC LIMIT {limit}"
    cursor.execute(q)
    book = cursor.fetchall()
    all_book = []
    for item in book:
        all_book.append(item)

    conn.close()
    if book is None:
        raise HTTPException(status_code=404, detail="No book in the database")
    return {"data":all_book}

@app.post("/books/", response_model=BookCreate)
async def create_book(book: BookCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO books (name, author_name, price, stock, publish_year) 
    VALUES (?, ?, ?, ?, ?)
    ''', (book.name, book.author_name, book.price, book.stock, book.publish_year))
    conn.commit()
    conn.close()
    return book

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(book)



@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    existing_book = cursor.fetchone()
    if existing_book is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.execute('''
        UPDATE books SET name = ?, author_name = ?, price = ?, stock = ?, publish_year = ?
        WHERE id = ?
    ''', (book.name, book.author_name, book.price, book.stock, book.publish_year, book_id))
    conn.commit()
    conn.close()
    return {"id": book_id, **book.dict()}




@app.delete("/books/{book_id}")
async def delete_book(book_id:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    if book is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return {"message": "Book deleted successfully"}




@app.post("/user/", response_model=User)
async def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (name, email, phone_no, password, is_admin) 
    VALUES (?, ?, ?, ?, ?)
    ''', (user.name, user.email, user.phone_no, user.password, user.is_admin))
    conn.commit()
    conn.close()
    return user



# @app.get("/insert_many")
# async def insert_many():
#     data = [
#     {
#         "name": "To Kill a Mockingbird",
#         "author_name": "Michelle Obama",
#         "price": 77.27,
#         "stock": 29,
#         "publish_year": 2003
#     },
#     {
#         "name": "All the Light We Cannot See",
#         "author_name": "S.E. Hinton",
#         "price": 80.65,
#         "stock": 41,
#         "publish_year": 1904
#     },
#     {
#         "name": "To Kill a Mockingbird",
#         "author_name": "Paulo Coelho",
#         "price": 41.28,
#         "stock": 19,
#         "publish_year": 1985
#     },
#     {
#         "name": "A Game of Thrones",
#         "author_name": "Stephen Chbosky",
#         "price": 67.21,
#         "stock": 41,
#         "publish_year": 1904
#     },
#     {
#         "name": "Little Fires Everywhere",
#         "author_name": "Yann Martel",
#         "price": 34.05,
#         "stock": 45,
#         "publish_year": 1912
#     },
#     {
#         "name": "The Girl on the Train",
#         "author_name": "Anthony Doerr",
#         "price": 36.36,
#         "stock": 16,
#         "publish_year": 1932
#     },
#     {
#         "name": "The Perks of Being a Wallflower",
#         "author_name": "Aldous Huxley",
#         "price": 5.39,
#         "stock": 33,
#         "publish_year": 1901
#     },
#     {
#         "name": "The Alchemist",
#         "author_name": "Gail Honeyman",
#         "price": 67.83,
#         "stock": 11,
#         "publish_year": 1954
#     },
#     {
#         "name": "Becoming",
#         "author_name": "Harper Lee",
#         "price": 86.82,
#         "stock": 15,
#         "publish_year": 1966
#     },
#     {
#         "name": "The Silent Patient",
#         "author_name": "Madeline Miller",
#         "price": 76.93,
#         "stock": 5,
#         "publish_year": 1913
#     },
#     {
#         "name": "The Girl on the Train",
#         "author_name": "Margaret Atwood",
#         "price": 71.0,
#         "stock": 2,
#         "publish_year": 1956
#     },
#     {
#         "name": "Jane Eyre",
#         "author_name": "Lois Lowry",
#         "price": 96.17,
#         "stock": 28,
#         "publish_year": 1919
#     },
#     {
#         "name": "The Handmaid's Tale",
#         "author_name": "Agatha Christie",
#         "price": 50.49,
#         "stock": 37,
#         "publish_year": 1920
#     },
#     {
#         "name": "1984",
#         "author_name": "Tara Westover",
#         "price": 59.95,
#         "stock": 38,
#         "publish_year": 1922
#     },
#     {
#         "name": "Becoming",
#         "author_name": "William Golding",
#         "price": 41.51,
#         "stock": 4,
#         "publish_year": 1991
#     },
#     {
#         "name": "The Silent Patient",
#         "author_name": "Aldous Huxley",
#         "price": 94.41,
#         "stock": 21,
#         "publish_year": 1907
#     },
#     {
#         "name": "The Handmaid's Tale",
#         "author_name": "Agatha Christie",
#         "price": 83.04,
#         "stock": 13,
#         "publish_year": 2021
#     },
#     {
#         "name": "The Underground Railroad",
#         "author_name": "William Golding",
#         "price": 95.58,
#         "stock": 7,
#         "publish_year": 1903
#     },
#     {
#         "name": "Harry Potter and the Sorcerer's Stone",
#         "author_name": "Harper Lee",
#         "price": 41.08,
#         "stock": 43,
#         "publish_year": 1951
#     },
#     {
#         "name": "Normal People",
#         "author_name": "Yann Martel",
#         "price": 88.77,
#         "stock": 19,
#         "publish_year": 1911
#     },
#     {
#         "name": "The Great Alone",
#         "author_name": "Richard Powers",
#         "price": 35.28,
#         "stock": 16,
#         "publish_year": 1933
#     },
#     {
#         "name": "The Underground Railroad",
#         "author_name": "Stephen Chbosky",
#         "price": 65.34,
#         "stock": 22,
#         "publish_year": 2022
#     },
#     {
#         "name": "The Catcher in the Rye",
#         "author_name": "Aldous Huxley",
#         "price": 62.87,
#         "stock": 27,
#         "publish_year": 1970
#     },
#     {
#         "name": "The Underground Railroad",
#         "author_name": "Cormac McCarthy",
#         "price": 21.65,
#         "stock": 18,
#         "publish_year": 1947
#     },
#     {
#         "name": "The Maze Runner",
#         "author_name": "Donna Tartt",
#         "price": 56.24,
#         "stock": 3,
#         "publish_year": 1979
#     },
#     {
#         "name": "The Overstory",
#         "author_name": "Stephen Chbosky",
#         "price": 8.15,
#         "stock": 44,
#         "publish_year": 1962
#     },
#     {
#         "name": "Big Little Lies",
#         "author_name": "Richard Powers",
#         "price": 7.97,
#         "stock": 11,
#         "publish_year": 1901
#     },
#     {
#         "name": "Divergent",
#         "author_name": "Lois Lowry",
#         "price": 75.51,
#         "stock": 24,
#         "publish_year": 1942
#     },
#     {
#         "name": "The Hunger Games",
#         "author_name": "Liane Moriarty",
#         "price": 79.02,
#         "stock": 36,
#         "publish_year": 1936
#     },
#     {
#         "name": "The Overstory",
#         "author_name": "Colson Whitehead",
#         "price": 55.98,
#         "stock": 41,
#         "publish_year": 1982
#     },
#     {
#         "name": "The Giver",
#         "author_name": "Yann Martel",
#         "price": 31.23,
#         "stock": 47,
#         "publish_year": 1929
#     },
#     {
#         "name": "Lord of the Flies",
#         "author_name": "Richard Powers",
#         "price": 23.31,
#         "stock": 36,
#         "publish_year": 2010
#     },
#     {
#         "name": "The Immortalists",
#         "author_name": "Delia Owens",
#         "price": 27.24,
#         "stock": 4,
#         "publish_year": 1994
#     },
#     {
#         "name": "Where the Crawdads Sing",
#         "author_name": "J.R.R. Tolkien",
#         "price": 33.87,
#         "stock": 25,
#         "publish_year": 1928
#     },
#     {
#         "name": "The Hunger Games",
#         "author_name": "Lois Lowry",
#         "price": 33.73,
#         "stock": 10,
#         "publish_year": 1998
#     },
#     {
#         "name": "Wuthering Heights",
#         "author_name": "Donna Tartt",
#         "price": 27.99,
#         "stock": 35,
#         "publish_year": 2009
#     },
#     {
#         "name": "The Underground Railroad",
#         "author_name": "Erin Morgenstern",
#         "price": 10.88,
#         "stock": 42,
#         "publish_year": 1991
#     },
#     {
#         "name": "Normal People",
#         "author_name": "Stieg Larsson",
#         "price": 58.55,
#         "stock": 35,
#         "publish_year": 1908
#     },
#     {
#         "name": "The Girl on the Train",
#         "author_name": "Erin Morgenstern",
#         "price": 26.63,
#         "stock": 33,
#         "publish_year": 1939
#     },
#     {
#         "name": "The Fault in Our Stars",
#         "author_name": "Stieg Larsson",
#         "price": 37.68,
#         "stock": 15,
#         "publish_year": 2020
#     },
#     {
#         "name": "Becoming",
#         "author_name": "Stieg Larsson",
#         "price": 61.56,
#         "stock": 8,
#         "publish_year": 1957
#     },
#     {
#         "name": "The Book Thief",
#         "author_name": "Gillian Flynn",
#         "price": 23.04,
#         "stock": 50,
#         "publish_year": 1900
#     },
#     {
#         "name": "The Kite Runner",
#         "author_name": "George R.R. Martin",
#         "price": 51.26,
#         "stock": 46,
#         "publish_year": 1918
#     },
#     {
#         "name": "The Road",
#         "author_name": "Stephen King",
#         "price": 62.89,
#         "stock": 5,
#         "publish_year": 2015
#     },
#     {
#         "name": "Little Fires Everywhere",
#         "author_name": "Alex Michaelides",
#         "price": 74.19,
#         "stock": 24,
#         "publish_year": 1936
#     },
#     {
#         "name": "Circe",
#         "author_name": "Colson Whitehead",
#         "price": 62.96,
#         "stock": 16,
#         "publish_year": 1911
#     },
#     {
#         "name": "The Shining",
#         "author_name": "George R.R. Martin",
#         "price": 41.93,
#         "stock": 48,
#         "publish_year": 1979
#     },
#     {
#         "name": "The Overstory",
#         "author_name": "Paula Hawkins",
#         "price": 24.89,
#         "stock": 50,
#         "publish_year": 1925
#     },
#     {
#         "name": "All the Light We Cannot See",
#         "author_name": "J.D. Salinger",
#         "price": 94.93,
#         "stock": 39,
#         "publish_year": 1983
#     },
#     {
#         "name": "The Handmaid's Tale",
#         "author_name": "John Green",
#         "price": 67.72,
#         "stock": 17,
#         "publish_year": 1957
#     }
#     ]

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     for book in data:
#         cursor.execute('''
#         INSERT INTO books (name, author_name, price, stock, publish_year) 
#         VALUES (?, ?, ?, ?, ?)
#         ''', (book['name'], book['author_name'], 
#               book['price'], book['stock'], book['publish_year']))
#         conn.commit()

#     conn.close()
