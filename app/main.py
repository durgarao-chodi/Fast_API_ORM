from fastapi import  FastAPI
from .database import engine
from . import models
from .routers import posts,users,auth,votes

#models.Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

# posts=[{"title":"title1","content":"content1","id":1},{"title":"title1","content":"content1","id":2}]
# def findPostById(id:int):
#     for item in posts:
#         if item['id']==id:
#             return item
@app.get("/")
async def get_root():
    return {"data":"success"}

