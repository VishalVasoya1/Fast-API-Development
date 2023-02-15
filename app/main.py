from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from postgre_connection import cursor,conn

app = FastAPI()

# Lot's of problem with body section : not in proper form, not getting validated, whatever they want they send.
# that's why get the data in proper schema use pydantic libary base model class.
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating  : Optional[int] = None


@app.get('/posts')
def get_post():
    cursor.execute("SELECT * FROM POSTS")
    data = cursor.fetchall()
    print(data)
    conn
    return {'fetch  ': data}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    # cursor.execute(f"insert into posts (title,content,published) values ({post.title},{post.content},{post.published})")
    cursor.execute("insert into posts (title,content,published) values (%s,%s,%s) returning *",(post.title,post.content,post.published))
    create_post = cursor.fetchone()
    conn.commit()
    return {'status': create_post}

# receive the data in the body section of the post
@app.post('/createpost')
def create_post(payload : dict = Body(...)):
    print(payload)
    return {'status':'post created succesfully'} 



# follow the schema of Post class.   
@app.post('/createpost')
def create_post(pay : Post):
    print(pay.title)
    print(pay.content)
    print(pay.published)
    print(pay.rating)
    print(pay.dict())
    # return {'msg': pay}
    return pay

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


# return the data to the user
@app.get('/returnuserpost')
def user_post():
    return {'data':my_post_details}

# add the user post to the database(list) which get from user by post method
@app.post('/getpostfromuser', status_code=status.HTTP_201_CREATED)
def create_post(pay : Post):
    post_dict = pay.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post_details.append(post_dict)
    return post_dict


# find the ppst by id
def find_post(id):
    for p in my_post_details:
        if p['id'] == id:
            return p


def find_index(id):
    for ind, p in enumerate(my_post_details):
        if p['id'] == id:
            return ind

# {id} -> path parameter
# use of response code 404 and raise exception of item not found.
# return message with item not found.
@app.get('/posts/{id}')
def get_post(id : int, response : Response):
    print(type(id)) # id -> string but in database -> int 
    # Here type conversion take place.
    post = find_post(id)
    if post is None:
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f'post with id {id} was not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f'post with id {id} was not found')
    return {'post_details': post}


# get the latest post oh the user
# one proble -> path = '/posts/latest'
# one think we have discussed in earlier that order matters in fast api so every time that you request that time it is going to above api request becasue both are same request and at place of id it consider as latest so that it throw a validation message.
# @app.get('/posts/latest') -> instead of executing this it is executing previous one because order matters.
@app.get('/posts/get/latest')
def get_latest_post():
    return {'details': my_post_details[len(my_post_details)-1]}
     

     
# for deleting the post use delete method with speific id.
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    # find the index in the list that has required id
    ind = find_index(id)
    if not ind:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post not found with id = {id}')
        # return {'msg':f'Post not found with id = {id}'}
    my_post_details.pop(ind)
    return {'msg':'post deleted succesfully. '}


# for updating title in the post using put method.
# put method is use when pass all of the field of the data. updation required all of the field of the data.
@app.put('/posts/{id}')
def update_post(id : int, post : Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Post is not found with id = {id}')
    post_dict = post.dict()
    post_dict['id'] = id
    my_post_details[index] = post_dict
    return {"msg" : f"Post has been updated with id = {id}"}

