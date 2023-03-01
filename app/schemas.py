from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

# Lot's of problem with body section : not in proper form, not getting validated, whatever they want they send.
# that's why get the data in proper schema use pydantic libary base model class.
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    # it is only working with dictionary by default. if you want it works with orm model like sqlalchemy
    class Config:
        orm_mode = True

# different model for different request.
# if you want user only update published column so you can create a structure for it.


class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str

# data that we embedded into our token
class TokenData(BaseModel):
    id : Optional[int] = None


class Vote(BaseModel):
    post_id : int
    dir : conint(le=1) # anything less than or equal to 1 are allowed.