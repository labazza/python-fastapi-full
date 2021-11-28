import time
from random import randrange

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status

# import this so you dont have to map column order to field order
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    # pydantic will convert number to sring
    # if title is for example 1 from post request
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


# can be in database.py
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi_full",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print(f"Error connecting: {error}")
        time.sleep(5)
# end

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite food", "content": "pizza", "id": 2},
]


def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# this simply gets the payload
# from fastapi.params import Body
# def create_posts(pay_load: dict = Body(...)):
def create_posts(post: Post):

    # post_dict = post.dict()
    # post_dict["ïd"] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    # do not use f string otherwise you are vulnerable to sql injection
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (
            post.title,
            post.content,
            post.published,
        ),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
# a path parameter is always a string unless i give it a type
def get_post(id: int, response: Response):

    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exists",
        )
    # you shouldnt be sending anything back with 204
    # return {"message": "post deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exists",
        )

    return {"data": updated_post}
