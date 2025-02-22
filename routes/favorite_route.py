from fastapi import APIRouter, Depends
from services.favorite_service import *
from entities.favorite_entity import favorite_entity
from sqlalchemy.orm import Session
from models.model import get_db

router_favorite = APIRouter()

@router_favorite.post("/add-favorite")
async def add_favorite(favorite: favorite_entity, db: Session = Depends(get_db) ):
    return await add_favorite_async(favorite, db)

@router_favorite.post("/remove-favorite")
async def remove_favorite(favorite: favorite_entity, db: Session = Depends(get_db) ):
    return await remove_favorite_async(favorite, db)

@router_favorite.get("/amount-favorite-by-post/{post_id}")
async def amount_favorite_by_post(post_id: int, db: Session = Depends(get_db) ):
    return await amount_favorite_by_post_async(post_id, db)

@router_favorite.get("/list-favorite-user/{user_id}")
async def list_favorite_user(user_id: int, db: Session = Depends(get_db) ):
    return await list_favorite_user_async(user_id, db)

@router_favorite.post("/favorite-exists")
async def favorite_exists(favorite: favorite_entity, db: Session = Depends(get_db) ):
    return await favorite_exists_async(favorite, db)


