from security.crypto import *
from dtos.login_dto import login_user_dto
from models.model import user_model as model
from fastapi.responses import JSONResponse

async def login_user_async(user: login_user_dto, db):
    try:
        if not user:
            return JSONResponse(content={"error":"user is required"}, status_code=400)
        
        db_entity = db.query(model).filter(model.email == user.email).first()
        
        if not db_entity:
            return False
            
        check: bool = await verify_password(user.password, db_entity.password)
            
        if check == False:
            return False
        
        return True
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)