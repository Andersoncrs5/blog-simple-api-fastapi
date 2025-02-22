from fastapi.responses import JSONResponse
from entities.user_entity import user_entity
from models.model import user_model
from security.crypto import *

async def email_free_async(email: str, db):
    try:
        if not email:
            return False  
        
        db_user = db.query(user_model).filter(user_model.email == email).first()
        
        if db_user:
            return True  
        
        return False  
    except Exception as e:
        return False  

async def get_async(id: int, db):
    try:
        if not isinstance(id, int) or id < 0:
            return JSONResponse(content={"error": "Id is required and must be a positive integer"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        return db_user
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def delete_async(id: int, db):
    try:
        if not isinstance(id, int) or id < 0:
            return JSONResponse(content={"error": "Id is required and must be a positive integer"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db.delete(db_user)
        db.commit()
        
        return {"message": "User deleted"}
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def create_async(user: user_entity, db):
    try:
        if not user:
            return JSONResponse(content={"error":"User not found"}, status_code=400)
        
        db_user = user_model(name=user.name,
            email=user.email, password=await hash_password(user.password))
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def update_async(user: user_entity, db):
    try:
        if not user:
            return JSONResponse(content={"error":"User not found"}, status_code=400)
            
        db_entity = db.query(user_model).filter(user_model.id == user.id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
            
        db_entity.name = user.name
        db_entity.password = await hash_password(user.password)
        db.commit()
        db.refresh(db_entity)
         
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def get_user_by_email_async(email: str, db):
    try:
        if not isinstance(email, str) or email == None:
            return JSONResponse(content={"error": "email is required"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.email == email).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        return db_user
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)