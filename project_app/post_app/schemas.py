import inspect
from pydantic import BaseModel
from typing import Union,Type
from fastapi import Form

# @as_form
# class Create_Post_Schema(BaseModel):
#   user_id:str
#   title:Union[str,None]=None

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
class Create_Post_Schema(BaseModel):
  title:Union[str,None]=None

class Create_Comment_Schema(BaseModel):
  post_id:str
  user_id:str
  content:Union[str,None]=None
  reply_id:Union[str,None]=None

@as_form
class Update_Post_Schema(BaseModel):
  title:Union[str,None]=None

class Update_Comment_Schema(BaseModel):
  content:Union[str,None]=None

class Create_Reply_Comment_Schema(BaseModel):
  user_id:str
  post_id:str
  content:Union[str,None]=None
  reply_id:Union[str,None]=None


  
