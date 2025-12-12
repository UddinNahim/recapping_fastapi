from fastapi import FastAPI, HTTPException ,status , Response
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

class UpdatedBooks(BaseModel):
    title: str
    author: str

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

@app.get("/books/{id}")
def get_book(id:int):
    cursor.execute("SELECT * FROM books where id = %s",(id,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,                            
        detail=f"book with id:{id} was not found"

        )
    return {"book_detail": book} 

@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int):
    # First delete related rows
    cursor.execute("DELETE FROM borrow_records WHERE book_id = %s", (id,))
    
    # Now delete book
    cursor.execute("DELETE FROM books WHERE id = %s RETURNING *", (id,))
    dlt_book = cursor.fetchone()

    conn.commit()

    if not dlt_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {id} not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/book/{id}")
def update_book(id:int,books:UpdatedBooks):
    cursor.execute("UPDATE books SET title = %s, author = %s where id = %s  RETURNING * " ,(books.title,books.author,id))
    updated_book = cursor.fetchone()
    conn.commit()
    if  updated_book == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"books not found with this id = {id}"
        )
    return updated_book

@app.put("/members/{id}")
def update_member(id:int, member:Member):
    cursor.execute("UPDATE members set name = %s , phone= %s WHERE id = %s RETURNING  *",(member.name,member.phone,id))
    updated_member = cursor.fetchone()
    conn.commit()
    if updated_member == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"member not found with this id = {id}"
        )
    return updated_member





@app.get("/members/{id}")
def get_member(id:int):
    cursor.execute("SELECT * FROM members where id = %s",(id,))
    member = cursor.fetchone()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Members not found with this id = {id}"
        )
    return {"member_detail": member}



    
