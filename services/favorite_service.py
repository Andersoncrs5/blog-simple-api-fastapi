from fastapi.responses import JSONResponse
from entities.favorite_entity import favorite_entity
from models.model import favorite_model, post_model, user_model

async def add_favorite_async(favorite: favorite_entity, db):
    try:
        if not favorite:
            return JSONResponse(content={"error": "favorite not found"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == favorite.user_id).first()
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db_post = db.query(post_model).filter(post_model.id == favorite.post_id).first()
        if not db_post:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
        
        db_favorite_exists = db.query(favorite_model).filter(
            favorite_model.user_id == favorite.user_id,
            favorite_model.post_id == favorite.post_id
        ).first()
        
        if db_favorite_exists:
            return JSONResponse(content={"error": "favorite already exists"}, status_code=409)
        
        db_favorite = favorite_model(user_id=favorite.user_id, post_id=favorite.post_id)
        db.add(db_favorite)
        db.commit()
        db.refresh(db_favorite)

        return db_favorite

    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def remove_favorite_async(favorite: favorite_entity, db):
    try:
        if not favorite:
            return JSONResponse(content={"error": "favorite not found"}, status_code=400)
        
        db_favorite_exists = db.query(favorite_model).filter(
            favorite_model.user_id == favorite.user_id,
            favorite_model.post_id == favorite.post_id
        ).first()
        
        if not db_favorite_exists:
            return JSONResponse(content={"error": "favorite not found"}, status_code=404)
        
        db.delete(db_favorite_exists)
        db.commit()

        return {"message": "favorite deleted"}
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def amount_favorite_by_post_async(post_id: int, db):
    try:
        if not isinstance(post_id, int) or post_id < 0:
            return JSONResponse(content={"error": "id post is required and must be a positive integer"}, status_code=400)
        
        favorite_count = db.query(favorite_model).filter(favorite_model.post_id == post_id).count()

        return {"post_id": post_id, "favorite_count": favorite_count}
    
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def list_favorite_user_async(user_id: int, db):
    try:
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db_posts = db.query(favorite_model).filter(favorite_model.user_id == user_id).all()

        return db_posts
    
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def favorite_exists_async(favorite: favorite_entity, db):
    try:
        db_favorite_exists = db.query(favorite_model).filter(
            favorite_model.user_id == favorite.user_id,
            favorite_model.post_id == favorite.post_id
        ).first()
        
        if not db_favorite_exists:
            return False
        
        return True
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)