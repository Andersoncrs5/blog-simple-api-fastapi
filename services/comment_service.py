from entities.comment_entity import comment_entity
from models.model import comment_model as model
from models.model import user_model
from models.model import post_model
from fastapi.responses import JSONResponse

async def create_async(user_id, post_id, comment: comment_entity, db):
    try:
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db_post = db.query(post_model).filter(post_model.id == post_id).first()
        if not db_post:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
        
        db_comment = model(
            name_user=db_user.name,
            content=comment.content,
            user_id=user_id,
            post_id=post_id
        )
        
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        
        return db_comment
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
      
async def delete_async(id: int, db):
    try:
        if not isinstance(id, int) or id < 0:
            return JSONResponse(content={"error": "Id is required and must be a positive integer"}, status_code=400)
            
        db_entity = db.query(model).filter(model.id == id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "comment not found"}, status_code=404)   
        
        db_comments_on_comment = db.query(model).filter(model.parent_id == id).all()  
        
        for comment in db_comments_on_comment:
            db.delete(comment)
         
        db.delete(db_entity)
        db.commit()
        
        return {"message":"Comment deleted!"}
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def get_async(id: int, db):
    try:
        if not isinstance(id, int) or id < 0:
            return JSONResponse(content={"error": "Id is required and must be a positive integer"}, status_code=400)
            
        db_entity = db.query(model).filter(model.id == id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "comment not found"}, status_code=404)   
         
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def update_async(comment: comment_entity, db):
    try:
        
        db_entity = db.query(model).filter(model.id == comment.id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "comment not found"}, status_code=404)
        
        db_entity.content = comment.content
        db_entity.is_updated = True
        
        db.commit()
        db.refresh(db_entity)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def get_all_comments_of_user_async(id:int, db):
    try:
        db_entity = db.query(user_model).filter(user_model.id == id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
            
        comments = db.query(model).filter(model.user_id == id).all()
        
        return comments
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
               
async def get_all_comments_of_post_async(post_id:int, db):
    try:
        db_entity = db.query(post_model).filter(post_model.id == post_id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
            
        comments = db.query(model).filter(
            model.post_id == post_id,
            model.parent_id == None,
            model.is_blocked == False
        ).all()
        
        return comments
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def create_comment_on_comment_async(id_comment, user_id, post_id, comment: comment_entity, db):
    try:
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db_post = db.query(post_model).filter(post_model.id == post_id).first()
        if not db_post:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
            
        db_comment_exists = db.query(model).filter(model.id == id_comment).first()
        if not db_comment_exists:
            return JSONResponse(content={"error": "comment not found"}, status_code=404)
        
        db_comment = model(
            name_user=db_user.name,
            content=comment.content,
            parent_id=id_comment,
            user_id=user_id,
            post_id=post_id
        )
        
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        
        return db_comment
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def get_all_comments_of_comment_async(id_comment: int, db):
    try:
        db_entity = db.query(model).filter((model.id == id_comment) & (model.is_blocked == False)).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "comment not found"}, status_code=404)

        comments = db.query(model).filter((model.parent_id == id_comment) & (model.is_blocked == False)).all()

        return comments
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

        
