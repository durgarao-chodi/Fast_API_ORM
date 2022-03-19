from .. import models,utils,schemas
from fastapi import Depends, status,HTTPException,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,oauth
from sqlalchemy.orm import Session


router=APIRouter(
    tags=['Authentication']
)

@router.post('/login',response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.Users).filter(models.Users.email==user_credentials.username).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalide Credentials')

    if not utils.verify(user_credentials.password,user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalide Credentials')
    access_token=oauth.create_access_token(data={"user_id":user.email})
    return {'access_token':access_token,
#     "token_type":"bearer"
    }