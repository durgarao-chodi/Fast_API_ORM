from .. import schemas,models,utils
from fastapi import Depends, status,HTTPException,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",response_model=schemas.UserOut)
def create_users(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_pwd=utils.hash(user.password)
    user.password=hashed_pwd
    new_user=models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_users(id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with {id} not available')
    return user