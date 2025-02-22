from entities.category_entity import category_entity
from models.model import category_model, user_model
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

def get_user(user_id: int, db: Session):
    """Função auxiliar para obter o usuário e verificar se ele é administrador."""
    db_user = db.query(user_model).filter(user_model.id == user_id).first()
    if not db_user:
        return JSONResponse(content={"error": "User not found"}, status_code=404)
    if not db_user.is_adm:
        return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
    return db_user

async def get_async(id: int, db: Session, user_id: int):
    try:
        if id < 0:
            return JSONResponse(content={"error": "Id must be a positive integer"}, status_code=400)
        
        user_check = get_user(user_id, db)
        if isinstance(user_check, JSONResponse):
            return user_check
        
        db_entity = db.query(category_model).filter(category_model.id == id).first()
        if not db_entity:
            return JSONResponse(content={"error": "Category not found"}, status_code=404)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def delete_async(id: int, db: Session, user_id: int):
    try:
        if id < 0:
            return JSONResponse(content={"error": "Id must be a positive integer"}, status_code=400)
        
        user_check = get_user(user_id, db)
        if isinstance(user_check, JSONResponse):
            return user_check
        
        db_entity = db.query(category_model).filter(category_model.id == id).first()
        if not db_entity:
            return JSONResponse(content={"error": "Category not found"}, status_code=404)
        
        db.delete(db_entity)
        db.commit()
        
        return {"message": "Category deleted"}
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def create_async(user_id: int, entity: category_entity, db: Session):
    try:
        if not entity:
            return JSONResponse(content={"error": "Category is required"}, status_code=400)
        
        user_check = get_user(user_id, db)
        if isinstance(user_check, JSONResponse):
            return user_check
        
        db_category = category_model(name=entity.name, name_user=user_check.name, user_id=user_id)
        
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        
        return db_category
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def update_async(id: int, entity: category_entity, db: Session, user_id: int):
    try:
        if not entity:
            return JSONResponse(content={"error": "Category is required"}, status_code=400)
        
        user_check = get_user(user_id, db)
        if isinstance(user_check, JSONResponse):
            return user_check
        
        db_entity = db.query(category_model).filter(category_model.id == id).first()
        if not db_entity:
            return JSONResponse(content={"error": "Category not found"}, status_code=404)
        
        db_entity.name = entity.name
        db.commit()
        db.refresh(db_entity)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def get_all_category_async(db: Session):
    try:
        categories = db.query(category_model).filter(category_model.is_actived == True).all()
        return categories
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def active_or_unactive_category_async(id: int, db: Session, user_id: int):
    try:
        if id < 0:
            return JSONResponse(content={"error": "Id must be a positive integer"}, status_code=400)
        
        user_check = get_user(user_id, db)
        if isinstance(user_check, JSONResponse):
            return user_check
        
        db_entity = db.query(category_model).filter(category_model.id == id).first()
        if not db_entity:
            return JSONResponse(content={"error": "Category not found"}, status_code=404)
        
        db_entity.is_actived = not db_entity.is_actived
        db.commit()
        db.refresh(db_entity)
        
        return {"message": "Category updated successfully", "is_actived": db_entity.is_actived}
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
