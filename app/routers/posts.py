from sqlalchemy import func
from .. import schemas,models,oauth
from fastapi import Depends, Response, status,HTTPException,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostsOut])
async def get_posts(db:Session=Depends(get_db),current_user:str=Depends(oauth.get_current_user)):
    print(current_user)
    # posts={}
    posts=db.query(models.Posts,func.count(models.Vote.user_id).label("Votes")).join(models.Vote,models.Vote.post_id==models.Posts.id,isouter=True).group_by(models.Posts.id).all()
    # posts=db.query(models.Posts).all()
    print(posts)
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Posts)
async def create_posts(post:schemas.CreatePosts,db:Session=Depends(get_db),current_user:str=Depends(oauth.get_current_user)):
    
    new_post=models.Posts(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}",response_model=schemas.Posts)
async def update_posts(id:int,update_post:schemas.CreatePosts,db:Session=Depends(get_db),current_user:str=Depends(oauth.get_current_user)):
    post_query=db.query(models.Posts).filter(models.Posts.id==id)
    post =post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} not available')
    
    if post.owner_id!=current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not autherized to perform requested action")
        
    post_query.update(update_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

@router.get("/{id}",response_model=schemas.PostsOut)
async def get_posts_by_id(id:int,db:Session=Depends(get_db),current_user:str=Depends(oauth.get_current_user)):
    post=db.query(models.Posts,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id==models.Posts.id,isouter=True).group_by(models.Posts.id).filter(models.Posts.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} not available')
    return post

@router.delete("/{id}")
async def get_posts_by_id(id:int,db:Session=Depends(get_db),current_user:str=Depends(oauth.get_current_user)):
    post_query=db.query(models.Posts).filter(models.Posts.id==id)
    post=post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} does not exist')
    
    if post.owner_id!=current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not autherized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)