from fastapi import APIRouter, Depends
from services.category_service import *
from entities.category_entity import category_entity
from sqlalchemy.orm import Session
from models.model import get_db

router_category = APIRouter()

@router_category.get("/get/{id}/{user_id}")
async def get(id: int, user_id: int, db: Session = Depends(get_db)):
    return await get_async(id, db, user_id)

@router_category.delete("/delete/{id}/{user_id}")
async def delete(id: int, user_id: int, db: Session = Depends(get_db)):  
    return await delete_async(id, db, user_id)

@router_category.post("/create/{user_id}")
async def create(user_id: int, entity: category_entity, db: Session = Depends(get_db)):
    return await create_async(user_id, entity, db)

@router_category.put("/update/{user_id}")
async def update(user_id: int, entity: category_entity, db: Session = Depends(get_db)):  
    return await update_async(entity)

@router_category.get("/get-all-category")
async def get_all_category(db: Session = Depends(get_db)):
    return await get_all_category_async(db)

@router_category.get("/active-or-unactive-category/{id_category}/{user_id}")
async def active_or_unactive_category(id_category: int, user_id: int, db: Session = Depends(get_db)): 
    return await active_or_unactive_category_async(id_category, db, user_id)
