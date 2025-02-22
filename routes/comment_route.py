from fastapi import APIRouter, Depends
from services.comment_service import *
from entities.comment_entity import comment_entity
from models.model import get_db
from sqlalchemy.orm import Session

router_comment = APIRouter()

@router_comment.get("/get/{id}")
async def get(id:int, db: Session = Depends(get_db) ):
    return await get_async(id, db)
    
@router_comment.get("/get-all-comments-of-comment/{id_comment}")
async def get_all_comments_of_comment(id_comment: int, db: Session = Depends(get_db)):
    return await get_all_comments_of_comment_async(id_comment, db)
    
@router_comment.delete("/delete/{id}")
async def delete(id:int,  db: Session = Depends(get_db) ):
    return await delete_async(id, db)
    
@router_comment.post("/create/{user_id}/{post_id}")
async def create(user_id:int, post_id:int,entity : comment_entity, db: Session = Depends(get_db) ):
    return await create_async(user_id, post_id,entity, db)
    
@router_comment.put("/update")
async def update(entity : comment_entity, db: Session = Depends(get_db) ):
    return await update_async(entity, db)
    
@router_comment.get("/get-all-comments-of-user/{id}")
async def get_all_comments_of_user(id:int, db: Session = Depends(get_db) ):
    return await get_all_comments_of_user_async(id, db)
    
    
@router_comment.get("/get-all-comments-of-post/{id}")
async def get_all_posts_of_user(id:int, db: Session = Depends(get_db) ):
    return await get_all_comments_of_post_async(id, db)
  
@router_comment.post("/create-comment-on-comment/{id_comment}/{user_id}/{post_id}")
async def create_comment_on_comment(id_comment:int,user_id:int, post_id:int,entity : comment_entity, db: Session = Depends(get_db) ):
    return await create_comment_on_comment_async(id_comment,user_id, post_id,entity, db)  
