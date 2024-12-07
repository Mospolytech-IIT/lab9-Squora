from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from database import SessionLocal, engine
import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.put("/users/{user_id}/email")
def update_user_email(user_id: int, new_email: str, db: Session = Depends(get_db)):
    return crud.update_user_email(db, user_id, new_email)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_post(db, post, user_id)

@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

@app.put("/posts/{post_id}/content")
def update_post_content(post_id: int, new_content: str, db: Session = Depends(get_db)):
    return crud.update_post_content(db, post_id, new_content)

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)

@app.get("/users", response_model=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/posts", response_model=HTMLResponse)
def list_posts(request: Request, db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return templates.TemplateResponse("posts.html", {"request": request, "users": posts})

@app.post("/users/")
def create_user_form(name: str, email: str, db: Session = Depends(get_db)):
    crud.create_user(db, schemas.UserCreate(name=name, email=email))
    return HTMLResponse(status_code=303, headers={"Location": "/users"})

@app.post("/users/{user_id}/delete")
def delete_user_form(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return HTMLResponse(status_code=303, headers={"Location": "/users"})

@app.post("/posts/")
def create_post_form(title: str, content: str, user_id: int, db: Session = Depends(get_db)):
    crud.create_post(db, schemas.PostCreate(title=title, content=content), user_id)
    return HTMLResponse(status_code=303, headers={"Location": "/posts"})

@app.post("/posts/{post_id}/delete")
def delete_post_form(post_id: int, db: Session = Depends(get_db)):
    crud.delete_post(db, post_id)
    return HTMLResponse(status_code=303, headers={"Location": "/posts"})