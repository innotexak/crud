from typing import Optional, List
from pydantic import BaseModel, Field

class PostModel(BaseModel):
    title: str
    author: str
    likes: int
    published: bool

class EditPostModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    likes: Optional[int] = None
    published: Optional[bool] = None

class PostCollection(BaseModel):
    posts: List[PostModel]