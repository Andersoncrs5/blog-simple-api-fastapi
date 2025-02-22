from fastapi.responses import JSONResponse
from models.model import user_model
from models.model import comment_model
from models.model import post_model

async def block_or_unblock_user_async(id_user, id_adm, db):
    try:
        db_adm = db.query(user_model).filter(user_model.id == id_adm).first()
        
        if not db_adm:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_adm.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_user = db.query(user_model).filter(user_model.id == id_user).first()
        
        if not db_user:
            return JSONResponse(content={"error": "db_entity not found"}, status_code=404)
        
        db_user.is_block = not db_user.is_block
        
        db.commit()
        db.refresh(db_user)
        
        return {"message": f"blocked:{db_user.is_block}"}
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def block_or_unblock_comment_async(id_comment: int, user_id: int, db):
    try:
        if not isinstance(id_comment, int) or id_comment < 0:
            return JSONResponse(content={"error": "id_comment must be a positive integer"}, status_code=400)
        
        if not isinstance(user_id, int) or user_id < 0:
            return JSONResponse(content={"error": "user_id must be a positive integer"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_user.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_comment = db.query(comment_model).filter(comment_model.id == id_comment).first()
        
        if not db_comment:
            return JSONResponse(content={"error": "Comment not found"}, status_code=404)
        
        db_comment.is_blocked = not db_comment.is_blocked
        db.commit()
        db.refresh(db_comment)
        
        return {"message": "Comment updated successfully", "is_blocked": db_comment.is_blocked}
    
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
  
async def list_comments_block_async(user_id:int, db):
    try:
        if not isinstance(user_id, int) or user_id < 0:
            return JSONResponse(content={"error": "user_id is required and must be a positive integer"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        if db_user.is_adm == False:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        comments = db.query(comment_model).filter(comment_model.is_blocked == True).all()
        
        return comments
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
 
async def list_post_blocked_async(user_id:int, db):
    try:
        if not isinstance(user_id, int) or user_id < 0:
            return JSONResponse(content={"error": "user_id is required and must be a positive integer"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        if db_user.is_adm == False:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        posts = db.query(post_model).filter(post_model.is_blocked == True).all()
        
        return posts
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def block_or_unblock_post_async(id_post: int, user_id: int, db):
    try:
        if not isinstance(id_post, int) or id_post < 0:
            return JSONResponse(content={"error": "id_post must be a positive integer"}, status_code=400)
        
        if not isinstance(user_id, int) or user_id < 0:
            return JSONResponse(content={"error": "user_id must be a positive integer"}, status_code=400)
        
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_user.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_post = db.query(post_model).filter(post_model.id == id_post).first()
        
        if not db_post:
            return JSONResponse(content={"error": "Post not found"}, status_code=404)
        
        db_comments = db.query(comment_model).filter(
            comment_model.post_id == id_post
        ).all()
        
        for comment in db_comments:
            comment.is_blocked_by_post = not comment.is_blocked_by_post
        
        db_post.is_blocked = not db_post.is_blocked
        
        db.commit()
        db.refresh(db_post)
        
        return {"message": "Post and comments updated successfully", "is_blocked": db_post.is_blocked}
    
    except Exception as e:
        db.rollback()  
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def is_post_blocked_async(id_post:int, db):
    try:
        if not isinstance(id_post, int) or id_post < 0:
            return JSONResponse(content={"error": "id of post is required and must be a positive integer"}, status_code=400)
            
        db_entity = db.query(post_model).filter(post_model.id == id_post).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
            
        if db_entity.is_blocked == False:
            return False
          
        return True
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def is_comment_blocked_async(id_comment:int, db):
    try:
        if not isinstance(id_comment, int) or id_comment < 0:
            return JSONResponse(content={"error": "id of comment is required and must be a positive integer"}, status_code=400)
            
        db_entity = db.query(comment_model).filter(comment_model.id == id_comment).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "comment not found"}, status_code=404)
            
        if db_entity.is_blocked == False:
            return False
        
        return True
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
               
async def find_user_by_email_async(email:str, id_user,db):
    try:
        db_adm = db.query(user_model).filter(user_model.id == id_user).first()
        
        if not db_adm:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_adm.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_entity = db.query(user_model).filter(user_model.email == email).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def list_all_user_async(id_user:int, db):
    try:
        db_user = db.query(user_model).filter(user_model.id == id_user).first()
        
        if not db_user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_user.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_users = db.query(user_model).all()
        
        return db_users
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def find_user_by_id_async(id:str, id_user,db):
    try:
        db_adm = db.query(user_model).filter(user_model.id == id_user).first()
        
        if not db_adm:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_adm.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_entity = db.query(user_model).filter(user_model.id == id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "user not found"}, status_code=404)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def list_all_post_async(id_user:int, db):
    try:
        db_user = db.query(user_model).filter(user_model.id == id_user).first()
        
        if not db_user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_user.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_posts = db.query(post_model).all()
        
        return db_posts
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def find_post_by_id_async(post_id:int , user_id:int ,db):
    try:
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_user.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_entity = db.query(post_model).filter(post_model.id == post_id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)

async def list_all_comments_async(user_id:int, db):
    try:
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_user.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_comments = db.query(comment_model).all()
        
        return db_comments
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)
        
async def find_comment_by_id_async(comment_id:int , user_id:int ,db):
    try:
        db_user = db.query(user_model).filter(user_model.id == user_id).first()
        
        if not db_user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        if not db_user.is_adm:
            return JSONResponse(content={"error": "You are not authorized"}, status_code=401)
        
        db_entity = db.query(comment_model).filter(comment_model.id == comment_id).first()
        
        if not db_entity:
            return JSONResponse(content={"error": "post not found"}, status_code=404)
        
        return db_entity
    except Exception as e:
        return JSONResponse(content={"error": f"Error: {str(e)}"}, status_code=500)        
