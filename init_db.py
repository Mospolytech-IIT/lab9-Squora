from database import engine, Base
from models import User, Post

Base.metadata.create_all(bind=engine)