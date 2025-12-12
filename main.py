from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Pydantic model
class Books(BaseModel):
    title: str
    author: str
    available: bool

class Member(BaseModel):
    name: str
    phone: str

    

# Database connection with retry loop
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=54876,
            database='library_management_system',
            user='postgres',
            password='postgres',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Successfully connected to PostgreSQL")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/books")
def bookRequest():
    cursor.execute(""" SELECT * FROM books """)
    data = cursor.fetchall()
    return {"Data": data}

@app.get("/members")
def members():
    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()
    return {"Data": data}

@app.post("/create_book")
def create_post_book(post:Books):
    cursor.execute("""INSERT INTO  books (title,author,available) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.author,post.available) )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.post("/members-add")
def member_create(data: Member):
    cursor.execute("INSERT INTO members (name,phone) VALUES(%s,%s) RETURNING *",(data.name,data.phone))
    new_data = cursor.fetchone()
    conn.commit()
    return {"data": new_data}