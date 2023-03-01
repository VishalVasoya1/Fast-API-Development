from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# @router.get('/',response_model=List[schemas.Post])
@router.get('/',response_model=List[schemas.PostOut])
def get_post(db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit:int=10, skip:int=0, search:Optional[str]=""):
    # cursor.execute("SELECT * FROM POSTS")
    # data = cursor.fetchall()
    # print(data)
    print(current_user.id)
    print(limit)
    print(skip)
    print(search)
    posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter().filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    # post = [{"Posts": {post.id, post.title, post.content},"votes":_} for post, _ in results]
        
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(f"insert into posts (title,content,published) values ({post.title},{post.content},{post.published})")
    # cursor.execute("insert into posts (title,content,published) values (%s,%s,%s) returning *",(post.title,post.content,post.published))
    # create_post = cursor.fetchone()
    # conn.commit()
    # print(current_user)
    # print(current_user.email)
    # print(current_user.id)
    # print(post.dict()) 

    create_post = models.Post(owner_id = current_user.id, **post.dict())

    # create_post = models.Post(title=post.title, content=post.content, published = post.published) # it's hard when you have 50 or more columns 
    db.add(create_post) # Post added to database
    db.commit() # commited the changes into database
    db.refresh(create_post) # retirve the post that we created and store back to the create_post variable
    return create_post



# {id} -> path parameter
# use of response code 404 and raise exception of item not found.
# return message with item not found.
@router.get('/{id}', response_model=schemas.Post)
def get_post(id : int, response : Response, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # print(type(id)) # id -> string but in database -> int 
    # # Here type conversion take place.
    # cursor.execute("SELECT * FROM POSTS WHERE ID=%s",(str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if post is None:
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f'post with id {id} was not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f'post with id {id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorized to perform requested action.')

    # conn.commit()
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("delete from posts where id = %s returning *",(str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorized to perform requested action.')

    post_query.delete(synchronize_session=False)
    db.commit()
    return {'status': f'succesfully deleted post with {id}'}


# for updating title in the post using put method.
# put method is use when pass all of the field of the data. updation required all of the field of the data.
@router.put('/{id}',response_model=schemas.Post)
def update_post(id : int, updated_post : schemas.PostBase, db : Session = Depends(get_db), current_user  : int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE POSTS SET TITLE=%s, CONTENT=%s, PUBLISHED=%s WHERE ID = %s returning * ",(post.title,post.content,post.published,str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Post is not found with id = {id}')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorized to perform requested action.')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post
    # return {"msg" : f"Post has been updated with id = {id}", "updated_post":post_query.first()}