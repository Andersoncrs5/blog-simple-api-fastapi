from fastapi import APIRouter, Depends
from services.like_service import *
from entities.like_entity import like_entity
from sqlalchemy.orm import Session
from models.model import get_db

router_like = APIRouter()

@router_like.post("/add-like")
async def add_like(like: like_entity, db: Session = Depends(get_db) ):
    return await add_like_async(like, db)

@router_like.post("/remove-like")
async def remove_like(like: like_entity, db: Session = Depends(get_db) ):
    return await remove_like_async(like, db)
    
@router_like.post("/like-exists")
async def like_exists(like: like_entity, db: Session = Depends(get_db) ):
    return await like_exists_async(like, db)

@router_like.get("/amount-like-by-post/{id_post}")
async def amount_like_by_post(id_post:int, db: Session = Depends(get_db) ):
    return await amount_like_by_post_async(id_post, db)
   
@router_like.get("/posts-user-gave-like/{id_user}")
async def posts_user_gave_like(id_user:int, db: Session = Depends(get_db) ):
    return await posts_user_gave_like_async(id_user, db)
   
   
    
"""
@router_like.delete("/delete/{id}")
async def delete(id:int, db: Session = Depends(get_db) ):
    return await metodo(id, db)
    
@router_like.post("/create")
async def create(entity : entity):
    return await metodo(entity)
    
@router_like.put("/update")
async def update(entity : user_entity):
    return await metodo(entity)
    
"""