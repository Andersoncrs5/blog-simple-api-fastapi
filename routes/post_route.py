from fastapi import APIRouter, Depends
from services.post_service import *
from entities.post_entity import post_entity
from models.model import get_db
from sqlalchemy.orm import Session

router_post = APIRouter()

@router_post.get("/get/{id}")
async def get(id:int, db: Session = Depends(get_db) ):
    return await get_async(id, db)

@router_post.get("/find-posts-by-category/{category}")
async def find_posts_by_category(category:str, db: Session = Depends(get_db) ):
    return await find_posts_by_category_async(category, db)
  
@router_post.get("/find-posts-by-title/{title}")
async def find_posts_by_title(title:str, db: Session = Depends(get_db) ):
    return await find_posts_by_title_async(title, db)
    
@router_post.delete("/delete/{id}")
async def delete(id:int, db: Session = Depends(get_db) ):
    return await delete_async(id, db)
    
@router_post.post("/create/{user_id}")
async def create(post : post_entity,user_id:int , db: Session = Depends(get_db) ):
    return await create_async(post, user_id, db)
    
@router_post.put("/update")
async def update(post : post_entity, db: Session = Depends(get_db) ):
    return await update_async(post, db)
    
@router_post.get("/get-all")
async def get_all(db: Session = Depends(get_db) ):
    return await get_all_async(db)
    
@router_post.get("/get-all-posts-of-user/{id}")
async def get_all_post_of_user(id:int, db: Session = Depends(get_db) ):
    return await get_all_posts_of_user_async(id, db)
    
