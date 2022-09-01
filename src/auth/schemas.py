from pydantic import BaseModel, validator
import re

 

class UserBase(BaseModel):
    email: str

class UserDisplay(UserBase):
    first_name : str 
    last_name : str 

class UserCreate(UserBase):

    password: str
    first_name : str 
    last_name : str 

    @validator("email")
    def valid_email(cls, value):
        match = re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", value)
        if match is not None :
            return value
        raise ValueError('Invalid email address')

    # @validator("password") # TODO : password constraint
    # def valid_password(cls, value):
        

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weak_password"
            }
        }    

class UserLogin(UserBase):

    password: str

    @validator("email")
    def valid_email(cls, value):
        match = re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", value)
        if match is not None :
            return value
        raise ValueError('Invalid email address')

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weak_password"
            }
        }    

class User(UserBase):
    id : int
    is_active : bool = True
    
    class Config:
        orm_mode = True


class Token(BaseModel): 
    access_token: str
    token_type: str
 

        