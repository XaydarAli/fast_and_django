from pydantic import BaseModel
from typing import Optional

class RegisterSchema(BaseModel):
    username:Optional[str]
    password:Optional[str]
    email:Optional[str]

class LoginSchema(BaseModel):
    username_or_email:Optional[str]
    password:Optional[str]

class ResetPasswordSchema(BaseModel):
    password:Optional[str]
    password2:Optional[str]




class PostCreateModel(BaseModel):
    id:Optional[str]
    caption:Optional[str]
    image_path:Optional[str]



class PostUpdateModel(BaseModel):
    caption:Optional[str]
    image_path: Optional[str]

