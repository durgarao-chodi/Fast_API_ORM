from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from sqlalchemy import true


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=true

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class BasePosts(BaseModel):
    title:str
    content:str
    published:bool=True

class CreatePosts(BasePosts):
    pass

class Posts(BasePosts):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut

    class Config:
        orm_mode=True
class PostsOut(BaseModel):
    Posts:Posts
    Votes:int
    class Config:
        orm_mode=True

class Token(BaseModel):
    access_token:str
    # token_type:str

class TokenData(BaseModel):
    user_id:EmailStr

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)