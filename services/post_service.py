from entities.post_entity import post_entity
from fastapi.responses import JSONResponse
from models.model import post_model as model
from models.model import user_model

async def find_posts_by_title_async(title: str, db):
    try:
        if not title:  
            return JSONResponse(content={"message": "Title is required"}, status_code=400)
        
        db_posts = db.query(model).filter(model.title.ilike(f"%{title}%")).all()
        
        return db_posts if db_posts else JSONResponse(content={"message": "No posts found"}, status_code=404)
    
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)


async def find_posts_by_category_async(category:str, db):
    try:
        if category == None:
            JSONResponse(content={"message":"Category is required"}, status_code=400)
        
        db_posts = db.query(model).filter(model.category == category).all()
        
        return db_posts
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def get_async(id: int, db):
    try:
        if not isinstance(id, int) or id < 0:
            return JSONResponse(content={"error": "Id is required and must be a positive integer"}, status_code=400)
        
        db_entity = db.query(model).filter(model.id == id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def delete_async(id: int, db):
    try:
        if not isinstance(id, int) or id < 0:
            return JSONResponse(content={"error": "Id is required and must be a positive integer"}, status_code=400)
            
        db_entity = db.query(model).filter(model.id == id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
        
        db.delete(db_entity)
        db.commit()
            
        return {"message": f"Post deleted"}
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def create_async(post: post_entity, user_id, db):
    try:
        if not post:
            return JSONResponse(content={"error": "post not found"}, status_code=400)
        
        db_entity = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        db_post = model(title=post.title, content=post.content, category=post.category, user_id=user_id, is_blocked=False)
        
        db.add(db_post)
        
        db.commit()
        db.refresh(db_post)
        
        return db_post
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def update_async(post: post_entity, db):
    try:
        if not post:
            return JSONResponse(content={"error":"post not found"}, status_code=400)
            
        db_post = db.query(model).filter(model.id == post.id).first()
        
        if not db_post:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
            
        db_post.title = post.title
        db_post.content = post.content
        db_post.category = post.category
           
        db.commit()
        db.refresh(db_post)
           
        return db_post
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def get_all_async(db):
    try:
        posts = db.query(model).filter(model.is_blocked == False).all()
        
        return posts
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def get_all_posts_of_user_async(id:int, db):
    try:
        
        if not isinstance(id, int) or id < 0:
            return JSONResponse(content={"error": "Id is required and must be a positive integer"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        posts = db.query(model).filter(model.user_id == id).all()
        
        return posts
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
        