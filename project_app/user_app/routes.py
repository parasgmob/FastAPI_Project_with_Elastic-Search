import asyncio
import time
from bson               import ObjectId
from typing             import Union
from .models            import User
from fastapi.security   import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.responses  import Response,JSONResponse
from fastapi            import APIRouter,Request,Depends,HTTPException,status,UploadFile,File,Header
from .schemas           import Signup,Validate_user,Send_OTP,Update_User
from fastapi.exceptions import RequestValidationError
from task               import send_mail,send_phone_verification
from fastapi.exceptions import RequestValidationError, ValidationError
from utility            import is_user_present,set_redis_key,verify_email_otp,authenticate_user,check_session,remove_redis_token
from message            import ERROR_USER_ALREAD_EXIST,SUCCESS_MSG,ERROR_INTERNAL_SERVER,INVALID_INPUT,ERROR_USER_NOT_FOUND,OTP_SENDED,INVALID_OTP,OTP_VERIFIED,INVALID_MODE,PHONE_OR_EMAIL_NOT_VERFIED,USER_NOT_LOGIN,USER_VALIDATED,INVALID_EMAIL_OR_PHONE_NO,Invalid_password
from elasticsearch1.client import es

user=APIRouter(
    tags=['user']
)

oauth_schema=OAuth2PasswordBearer(tokenUrl='token')



@user.post('/token')
async def token(token:OAuth2PasswordRequestForm=Depends()):
    is_user_valid=authenticate_user(token)
    if is_user_valid==False:
        raise HTTPException(status_code=404, detail="Not authorised")
    else:
        HTTPException(status_code=200, detail="Authorised")


def get_user(token: str = Depends(oauth_schema)):
      pass
    
@user.post('/auth/signup')
async def signup(request:Signup):
    try:
        if is_user_present(request.phone_no,request.email):
            return Response(ERROR_USER_ALREAD_EXIST)
        user_obj=User(full_name=request.full_name,phone_no=request.phone_no,email=request.email,country_code=request.country_code,gender=request.gender,password=request.password)
        user_obj.validate()
        user_obj.save()
        #asyncio.create_task(send_mail(request.email))
        return Response(SUCCESS_MSG)
    except (ValueError, AttributeError, AssertionError) as error:
        return Response(str(error))
    except Exception as e:
        return Response(ERROR_INTERNAL_SERVER +str(e))
    
@user.post('/auth/validate_user/')
def validate_user(request:Validate_user,is_authorised:str=Depends(get_user)):
    try:
        password=request.password
        user_obj=User.objects(email=request.email,phone_no=request.phone_no)
        if len(user_obj)==0 :
            return JSONResponse(INVALID_EMAIL_OR_PHONE_NO)
        
        if user_obj[0].password != password:
            return JSONResponse(Invalid_password)
        if request.mode=="login":
            if user_obj[0].is_email_verified==False or user_obj[0].is_phone_verified==False:
                return JSONResponse(PHONE_OR_EMAIL_NOT_VERFIED)
            token=set_redis_key(id=user_obj[0].id)
            data={
                "access_token":token
            }
            return JSONResponse(data)
        elif request.mode=="signup":
            if verify_email_otp(request.email,request.email_OTP):
                user_obj.update(__raw__={'$set': {'is_email_verified': True,'is_active':True}})
                token=set_redis_key(id=user_obj[0].id)
                data={
                "access_token":token
                }
                return JSONResponse(data)
            else:
                return JSONResponse(INVALID_OTP)  
    except (ValueError, AttributeError, AssertionError) as error:
           return Response(error)
    except Exception as e:
        User.objects(id=user_obj[0].id).delete()
        return Response(ERROR_INTERNAL_SERVER +"   "+str(e) )    
        
        
@user.post('/auth/send_otp') 
async def send_otp(request:Send_OTP,is_authorised:str=Depends(get_user)):
    try:
        email_id=request.email
        phone_no=request.phone_no
        password=request.password
        if email_id==None or phone_no==None or password==None:
            return JSONResponse(INVALID_INPUT)
        user_obj=User.objects(email=email_id,phone_no=phone_no,password=password)
        if len(user_obj)==0:
            return JSONResponse(ERROR_USER_NOT_FOUND)
        if len(user_obj)==1:
            await asyncio.create_task(send_mail(user_obj[0].email))
            return JSONResponse(OTP_SENDED)
    except (ValueError, AttributeError, AssertionError) as error:
           return Response(error)
    except Exception as e:
           return Response(ERROR_INTERNAL_SERVER)   
       
@user.post('/auth/update_user') 
async def update_user(token:str= Header(),user_image:Union[UploadFile,None]=File(default=None)):
    try:
        session_result,id=check_session(token,return_Id=True)
        if session_result:
            user_obj=User.objects(id=id)
            file_loc="/home/mobcoder/Desktop/social_app/fastapi-socialapp/app/media"+str(user_image.filename)
            with open(file_loc ,"wb") as ufile:
                ufile.write(user_image.file.read())
            user_obj.update(__raw__={'$set': {'profile_photo': file_loc}})    
            return JSONResponse({"msg":"success","status_code":200})
        else:
            return Response(USER_NOT_LOGIN)
    except (ValueError, AttributeError, AssertionError) as error:
           return Response(error)
    except Exception as e:
           return Response(ERROR_INTERNAL_SERVER)     


@user.get('/auth/user_info/')
async def user_info(token: Union[str, None] = Header(default=None)):
    id="63bc088bbff5017694064b8d"
    # print(type(ObjectId(id)))
    # session_result,id=check_session(token,return_Id=True)
    # if session_result==False or id==None:
    #     return Response(USER_NOT_LOGIN)
    print('!!!!!!!!!!!!!!_________________________')
    # test = User.objects.raw_query(id='63bc088bbff5017694064b8d')
    
    # print (test.id, 'akdakjsbdkjasbdkjasbd')
    
    user_obj=User.objects.get(__raw__={'_id':ObjectId(id)}).only('full_name','email','phone_no')
    print(user_obj, 'sasdbkajbsdkjabsdkj')
    # if len(user_info)==0:
    #    return JSONResponse("user not found")
    # # data=get_user_data(user_info)
    
    return JSONResponse("user success get info")

@user.delete('/auth/logout')
async def logout(token: Union[str, None] = Header(default=None)):
    try:
        session_result,id=check_session(token,return_Id=True)
        if session_result==False or id==None:
            return Response(USER_NOT_LOGIN)
        if remove_redis_token(id,token):
            return("user logout")
        else:
            return("Unsuccessfull logout")
    except (ValueError, AttributeError, AssertionError) as error:
           return Response(error)
    except Exception as e:
           return Response(ERROR_INTERNAL_SERVER) 
     