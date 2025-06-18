import sqlite3

def init_db():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            purchase_date TEXT,
            cost REAL,
            audiobook_link TEXT,
            status TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_book(data):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO books (title, author, genre, purchase_date, cost, audiobook_link, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_book(book_id, updated_data):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute('''
        UPDATE books SET title=?, author=?, genre=?, purchase_date=?, cost=?, audiobook_link=?, status=?, notes=?
        WHERE id=?
    ''', (*updated_data, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

