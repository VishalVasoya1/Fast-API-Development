from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from app.models import PostBase

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


# This is just for the testing of sqlalchemy, models and databse.
# @app.get('/sqlalchemy')
# def test_posts(db : Session = Depends(get_db)):
#     # grab every single entry from the database
#     posts = db.query(models.Post).all()
#     return {"status":posts}


# store the data that we received from the user for after use.
my_post_details = [
    {
        'title':'nandi hill',
        'content':'nature explorer',
        'id':100
    },
    {
        'title':'iskon temple',
        'content':'getting blessed by god',
        'id':101
    }
]

# follow the schema of Post class.   
@app.post('/createpost')
def create_post(pay : PostBase):
    print(pay.title)
    print(pay.content)
    print(pay.published)
    print(pay.rating)
    print(pay.dict())
    # return {'msg': pay}
    return pay


# return the data to the user
@app.get('/returnuserpost')
def user_post():
    return {'data':my_post_details}


# get the latest post oh the user
# one proble -> path = '/posts/latest'
# one think we have discussed in earlier that order matters in fast api so every time that you request that time it is going to above api request becasue both are same request and at place of id it consider as latest so that it throw a validation message.
# @app.get('/posts/latest') -> instead of executing this it is executing previous one because order matters.
@app.get('/posts/get/latest')
def get_latest_post():
    return {'details': my_post_details[len(my_post_details)-1]}
     
# find the ppst by id
def find_post(id):
    for p in my_post_details:
        if p['id'] == id:
            return p
     
# for deleting the post use delete method with speific id.
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    # find the index in the list that has required id
    ind = find_post(id)
    if not ind:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post not found with id = {id}')
        # return {'msg':f'Post not found with id = {id}'}
    my_post_details.pop(ind)
    return {'msg':'post deleted succesfully. '}

# receive the data in the body section of the post
@app.post('/createpost')
def create_post(payload : dict = Body(...)):
    print(payload)
    return {'status':'post created succesfully'} 