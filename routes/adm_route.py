from fastapi import APIRouter, Depends
from services.adm_service import *
from sqlalchemy.orm import Session
from models.model import get_db

router_adm = APIRouter()

@router_adm.get("/block-or-unblock-comment/{id_comment}/{user_id}")
async def block_or_unblock_comment(id_comment:int, user_id:int, db: Session = Depends(get_db)):
    return await block_or_unblock_comment_async(id_comment, user_id, db)

@router_adm.get("/block-or-unblock-post/{id_post}/{user_id}")
async def block_or_unblock_post(id_post:int, user_id:int, db: Session = Depends(get_db)):
    return await block_or_unblock_post_async(id_post, user_id, db)

@router_adm.get("/list-comments-block/{user_id}")
async def list_comments_block(user_id:int, db: Session = Depends(get_db)):
    return await list_comments_block_async(user_id, db)

@router_adm.get("/list-post-blocked/{user_id}")
async def list_post_blocked(user_id:int, db: Session = Depends(get_db)):
    return await list_post_blocked_async(user_id, db)

@router_adm.get("/is-post-blocked/{id_post}")
async def is_post_blocked(id_post:int, db: Session = Depends(get_db)):
    return await is_post_blocked_async(id_post, db)

@router_adm.get("/is-comment-blocked/{id_comment}")
async def is_comment_blocked(id_comment:int, db: Session = Depends(get_db)):
    return await is_comment_blocked_async(id_comment, db)

@router_adm.get("/find-user-by-email/{email}/{id_user}")
async def find_user_by_email(email:str, id_user:int, db: Session = Depends(get_db)):
    return await find_user_by_email_async(email, id_user, db)

@router_adm.get("/list-all-user/{id_user}")
async def list_all_user(id_user:int, db: Session = Depends(get_db)):
    return await list_all_user_async(id_user, db)

@router_adm.get("/find-user-by-id/{id}/{id_user}")
async def find_user_by_id(id:int, id_user:int, db: Session = Depends(get_db)):
    return await find_user_by_id_async(id, id_user, db)

@router_adm.get("/list-all-posts/{id_user}")
async def list_all_post(id_user:int, db: Session = Depends(get_db)):
    return await list_all_post_async(id_user, db)

@router_adm.get("/find-post-by-id/{id}/{id_user}")
async def find_post_by_id(id:int, id_user:int, db: Session = Depends(get_db)):
    return await find_post_by_id_async(id, id_user, db)

@router_adm.get("/block-or-unblock-user/{id_user}/{id_adm}")
async def block_or_unblock_user(id_user:int, id_adm:int, db: Session = Depends(get_db)):
    return await block_or_unblock_user_async(id_user, id_adm, db)

@router_adm.get("/list_all_comments/{user_id}")
async def list_all_comments(user_id:int, db: Session = Depends(get_db)):
    return await list_all_comments_async(user_id, db)

@router_adm.get("/find-comment-by-id/{id}/{id_user}")
async def find_comment_by_id(id:int, id_user:int, db: Session = Depends(get_db)):
    return await find_comment_by_id_async(id, id_user, db)
