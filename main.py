from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from routes.user_route import router_user 
from routes.post_route import router_post
from routes.comment_route import router_comment
from routes.category_route import router_category
from routes.login_route import router_login
from routes.adm_route import router_adm
from routes.like_route import router_like
from routes.favorite_route import router_favorite
from models.model import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(router_favorite, prefix="/favorite", tags=["Favorities"])
app.include_router(router_like, prefix="/like", tags=["Likes"])
app.include_router(router_adm, prefix="/adm", tags=["Adm-controller"])
app.include_router(router_category, prefix="/category", tags=["Categories"])
app.include_router(router_comment, prefix="/comment", tags=["Comments"])
app.include_router(router_post, prefix="/post", tags=["Posts"])
app.include_router(router_user, prefix="/user", tags=["Users"])
app.include_router(router_login, prefix="/login", tags=["login"])

init_db()
