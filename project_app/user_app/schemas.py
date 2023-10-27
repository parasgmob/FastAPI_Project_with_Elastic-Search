import re
import inspect
from fastapi   import Form
from typing    import Union,Type
from enum      import Enum
from message   import INVALID_NAME,INVALID_PHONE_NO,INVALID_EMAIL,INVALID_PASSWORD_LENGTH,INVALID_PASSWORD
from pydantic  import BaseModel,EmailStr,Field,validator
from .isValidField import *
# from typing import

class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    
class Signup(BaseModel):
    full_name:str
    phone_no:int
    email:Union[EmailStr,None]=None
    country_code:int
    gender: Gender = Field(None, alias='Gender')
    password:str
    
    _normalize_full_name=validator('full_name',allow_reuse=True)(valid_name)
    _normalize_phone_no=validator('phone_no',allow_reuse=True)(valid_phone_no)
    _normalize_email=validator('email',allow_reuse=True)(valid_email)
    _normalize_password=validator('password',allow_reuse=True)(valid_password)
    _normalize_country_code=validator('country_code',allow_reuse=True)(valid_country_code)
    _normalize_gender=validator('gender',allow_reuse=True)(valid_gender)
     

class Mode(str,Enum):
    login='login'
    signup='signup'
    
class Validate_user(BaseModel):
    mode:Mode = Field(None, alias='Mode')
    email_OTP:int
    phone_no:int
    email:EmailStr
    password:str
    country_code:Union[int,None]
    
    _normalize_phone_no=validator('phone_no',allow_reuse=True)(valid_phone_no)
    _normalize_email=validator('email',allow_reuse=True)(valid_email)
    _normalize_password=validator('password',allow_reuse=True)(valid_password)
    _normalize_country_code=validator('country_code',allow_reuse=True)(valid_country_code)
    
    
class Send_OTP(BaseModel):
    email:EmailStr
    phone_no:int
    password:str    
    
    # _normalize_phone_no=validator('phone_no',allow_reuse=True)(valid_phone_no)
    _normalize_email=validator('email',allow_reuse=True)(valid_email)
    _normalize_password=validator('password',allow_reuse=True)(valid_password)
    


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        new_parameters.append(
             inspect.Parameter(
                 model_field.alias,
                 inspect.Parameter.POSITIONAL_ONLY,
                 default=Form(...) if model_field.required else Form(model_field.default),
                 annotation=model_field.outer_type_,
             )
         )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls

@as_form
class Update_User(BaseModel):
    token:str
   

    