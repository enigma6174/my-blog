from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "id": 1,
        "title": "Hello World",
        "content": "The quick brown fox jumps over the lazy dog",
        "rating": 3
    },
    {
        "id": 2,
        "title": "Lorem Ipsum",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    }
]


def find_post(pid):
    for post in my_posts:
        if post["id"] == pid:
            return post
    return None


def find_post_index(pid):
    for index, post in enumerate(my_posts):
        if post["id"] == pid:
            return index
    return None


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts")
async def create_post(payload: Post, response: Response):
    new_post = payload.dict()
    try:
        new_post["id"] = randrange(0, 1000000)
        my_posts.append(new_post)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"[ERR] {e}")
    else:
        response.status_code = status.HTTP_201_CREATED
        return {"data": new_post}


@app.get("/posts/{pid}")
async def get_post(pid: int):
    post = find_post(int(pid))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for id {pid}")
    return {"data": post}


@app.delete("/posts/{pid}")
async def delete_post(pid: int):
    try:
        index = find_post_index(pid)
        my_posts.pop(index)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"[ERR] {e}")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{pid}")
def update_post(pid: int, payload: Post):
    try:
        index = find_post_index(pid)
        updated_post = payload.dict()
        updated_post["id"] = pid
        my_posts[index] = updated_post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")
    else:
        return {"data": updated_post}
