from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, utils, schemas
from database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate,db : Session = Depends(get_db)):
    
    # hash the password -> user.passowrd
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())

    # create_post = models.Post(title=post.title, content=post.content, published = post.published) # it's hard when you have 50 or more columns 
    db.add(new_user) # Post added to database
    db.commit() # commited the changes into database
    db.refresh(new_user) # retirve the post that we created and store back to the create_post variable
    return new_user


@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with {id} is not available')
    
    return user

