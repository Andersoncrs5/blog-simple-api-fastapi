from fastapi import APIRouter, Depends
from dtos.login_dto import login_user_dto
from services.login_service import *
from models.model import get_db
from sqlalchemy.orm import Session

router_login = APIRouter()

@router_login.post("/login")
async def login_user(user: login_user_dto, db: Session = Depends(get_db)):
    return await login_user_async(user, db)