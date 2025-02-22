from fastapi import APIRouter, Depends
from services.user_service import *
from entities.user_entity import user_entity
from models.model import get_db
from sqlalchemy.orm import Session

router_user = APIRouter()

@router_user.get("/get/{id}")
async def get(id:int, db: Session = Depends(get_db) ):
    return await get_async(id, db)
    
@router_user.delete("/delete/{id}")
async def delete(id:int, db: Session = Depends(get_db) ):
    return await delete_async(id, db)
    
@router_user.post("/create")
async def create(user: user_entity, db: Session = Depends(get_db) ):
    return await create_async(user, db)
    
@router_user.put("/update")
async def update(user: user_entity, db: Session = Depends(get_db) ):
    return await update_async(user, db)
    
@router_user.get("/get-user-by-email/{email}")
async def get_user_by_email(email:str, db: Session = Depends(get_db) ):
    return await get_user_by_email_async(email, db)
    
@router_user.get("/email-free/{email}")
async def email_free(email: str, db: Session = Depends(get_db)):
    return await email_free_async(email, db)
    