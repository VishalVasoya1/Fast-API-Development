from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


# get request function with path operation.
# When we are retriving the data that time we used get method.
@app.get('/items')
async def root():
    return {'message':'Hello World'}  


# get request function with path operation.
@app.get('/')
def root():
    return {'code':'succesfully', 'other' : 'way of sepeate'}
   
# post request function with with path operation.
# post method send the data to the server which is send by user and response return back to the user.
@app.get('/posts')
def get_posts():
    return {'data':"This is your posts"}
