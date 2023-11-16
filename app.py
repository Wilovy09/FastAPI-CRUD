from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Text, Optional
import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

class Post(BaseModel):
    id: Optional[str]
    title: str
    autor: str
    content: Text
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    published_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    published: bool = False

@app.get("/")
def read_root():
    return {"go-to": "/docs"}

@app.get("/posts")
def get_post():
    return posts

@app.post("/posts")
def add_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get("/posts/{post_id}")
def get_post_by_id(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            posts.pop(index)
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{post_id}")
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            posts[index]['title'] = updatedPost.title
            posts[index]['content'] = updatedPost.content
            posts[index]['autor'] = updatedPost.autor
            return {"message": "Post updated successfully"}
    raise HTTPException(status_code=404, detail="Post not found")