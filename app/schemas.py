from pydantic import BaseModel , EmailStr
from datetime import datetime

#---------------------------
# User Schema
#---------------------------

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at : datetime

    class Config:
        from_attributes = True


#--------------------
# Auth Schema
#--------------------

class Token(BaseModel):
    access_token: str
    token_type: str ="bearer"

class LoginRequest(BaseModel):
    email : EmailStr
    password: str


#-------------------------
# Document Schema
#-------------------------

class DocumentResponse(BaseModel):
    id: int
    filename: str

    class config:
        from_attributes = True


#-------------------------
# Q&A Schema
#-------------------------

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    