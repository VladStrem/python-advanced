from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime
import enum


class PostStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class PostBase(BaseModel):
    title: str
    content: str
    published: PostStatus = PostStatus.DRAFT


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[PostStatus] = None


class PostInDB(PostBase):
    id: UUID4
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_superuser: Optional[bool] = False

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserAuth(BaseModel):
    email: EmailStr
    password: str
