from pydantic import BaseModel
from typing import Optional


class ConfigBase(BaseModel):
    authjwt_secret_key:str='34237612c8feadb9c9dd530a7ba005631a84b50b3a09bab3ac500b7e48dbcf08'


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

