from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import schemas
import utils
from typing import Optional, List
from random import randrange
from postgre_connection import cursor,conn
from sqlalchemy.orm import Session
import schemas, utils, models
from database import get_db, engine
from routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)



