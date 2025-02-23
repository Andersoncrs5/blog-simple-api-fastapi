from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, func, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/blog_simple_api_fast"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class user_model(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True)
    password = Column(String(100))
    is_adm = Column(Boolean, default=False)
    is_block = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    categories = relationship("category_model", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("post_model", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("comment_model", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("log_model", back_populates="admin", cascade="all, delete-orphan")
    likes = relationship("like_model", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("favorite_model", back_populates="user", cascade="all, delete-orphan")

class post_model(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300))
    content = Column(String(3000))
    category = Column(String(300))
    is_blocked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("user_model", back_populates="posts")

    comments = relationship("comment_model", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("like_model", back_populates="post", cascade="all, delete-orphan")
    favorites = relationship("favorite_model", back_populates="post", cascade="all, delete-orphan")

class like_model(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("user_model", back_populates="likes")
    post = relationship("post_model", back_populates="likes")

class favorite_model(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("user_model", back_populates="favorites")
    post = relationship("post_model", back_populates="favorites")

class comment_model(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    name_user = Column(String(100))
    content = Column(String(300))
    parent_id = Column(Integer)
    is_blocked = Column(Boolean, default=False)
    is_blocked_by_post = Column(Boolean, default=False)
    is_updated = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("user_model", back_populates="comments")

    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("post_model", back_populates="comments")

class category_model(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True)
    name_user = Column(String(100))
    is_actived = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("user_model", back_populates="categories")

class log_model(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(255), nullable=False)
    target_id = Column(Integer, nullable=False)
    target_type = Column(Enum('post', 'comment', 'user', name='target_type_enum'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    admin = relationship("user_model", back_populates="logs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
