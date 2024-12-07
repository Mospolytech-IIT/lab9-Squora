from sqlalchemy.orm import Session
import models

def create_user(db: Session, username: str, email: str, password: str):
    user = models.User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_post(db: Session, title: str, content: str, user_id: int):
    post = models.Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_users(db: Session):
    return db.query(models.User).all()

def get_posts(db: Session):
    return db.query(models.Post).all()

def update_user_email(db: Session, user_id: int, new_email: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
    return user

def delete_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()