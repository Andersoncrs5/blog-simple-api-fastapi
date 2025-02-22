from fastapi.responses import JSONResponse
from entities.like_entity import like_entity
from models.model import like_model
from models.model import post_model
from models.model import user_model

async def add_like_async(like: like_entity, db):
    try:
        if not like:
            return JSONResponse(content={"error":"entity not found"}, status_code=400)
        
        db_like_exists = db.query(like_model).filter(
                like_model.post_id == like.post_id, 
                like_model.user_id == like.user_id 
            ).first()
        
        if db_like_exists:
            return JSONResponse(content={"error": "like already exists"}, status_code=404)
        
        db_user = db.query(user_model).filter(user_model.id == like.user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db_post = db.query(post_model).filter(post_model.id == like.post_id).first()
        
        if not db_post:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
        
        db_like = like_model(user_id=like.user_id, post_id=like.post_id)
        
        db.add(db_like)
        db.commit()
        db.refresh(db_like)

        return db_like
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def remove_like_async(like: like_entity, db):
    try:
        if not like:
            return JSONResponse(content={"error":"like is required"}, status_code=400)
        
        db_like = db.query(like_model).filter(
                like_model.post_id == like.post_id, 
                like_model.user_id == like.user_id 
            ).first()
        
        if not db_like:
            return JSONResponse(content={"error": "like not found"}, status_code=404)
        
        db.delete(db_like)
        db.commit()
        
        return {"message":"like deleted!"}
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def amount_like_by_post_async(post_id: int, db):
    try:
        if not isinstance(post_id, int) or post_id < 0:
            return JSONResponse(content={"error": "id post is required and must be a positive integer"}, status_code=400)
        
        like_count = db.query(like_model).filter(like_model.post_id == post_id).count()

        return {"post_id": post_id, "like_count": like_count}
        
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def like_exists_async(like: like_entity, db):
    try:
        if not like:
            return JSONResponse(content={"error":"like is required"}, status_code=400)
        
        db_like_exists = db.query(like_model).filter(
                like_model.post_id == like.post_id, 
                like_model.user_id == like.user_id 
            ).first()
        
        if not db_like_exists:
            return False
        
        return True
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def posts_user_gave_like_async(user_id:int, db):
    try:
        
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db_posts = db.query(like_model).filter(like_model.user_id == user_id).all()
        
        return db_posts
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        

