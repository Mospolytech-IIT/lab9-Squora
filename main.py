from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import crud
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/")
def create_new_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    return crud.create_user(db, username, email, password)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/posts/")
def create_new_post(title: str, content: str, user_id: int, db: Session = Depends(get_db)):
    return crud.create_post(db, title, content, user_id)

@app.get("/posts/")
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

@app.delete("/posts/{post_id}")
def delete_existing_post(post_id: int, db: Session = Depends(get_db)):
    crud.delete_post(db, post_id)
    return {"message": "Post deleted"}