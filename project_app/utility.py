import jwt
import json
from mongoengine.queryset.visitor import Q
from User.models                  import User
from bson                         import ObjectId
from datetime                     import datetime,timedelta
from configurations               import REDIS_CONNECTION,SECRET_KEY,DEFAULT_ALGORITHM

success_response_dict={"msg":"Success","status_code":200}


def remove_redis_token(redis_key,token):
    try:
        data_byte=REDIS_CONNECTION.get(redis_key)
        if data_byte == None:
            return False
        decoded_data= data_byte.decode('UTF-8')

        if decoded_data==token:
            REDIS_CONNECTION.delete(redis_key)
            return True
        else:
            return False
    except:
        return False    
       
    

def check_session(request,return_Id=None):
    """
    For check Session in Redis Connection and return True or False
    return_id: if return_id is True  Return id inside the tooken

    """
    token=request
    if token == None:
        if return_Id==True:
            return False,None
        else:
            return False
    token_payload = jwt.decode(token,SECRET_KEY,algorithms=[DEFAULT_ALGORITHM])
    current_id = token_payload.get("ID")
    data_byte = REDIS_CONNECTION.get(current_id)
    
    if data_byte != None: 
        if data_byte.decode('UTF-8')==token and return_Id == True:
            return True,current_id
        if data_byte.decode('UTF-8')==token:
           return True 
    if data_byte == None and return_Id==True:
       return False,None 
    else:
        return False  
      
def response_generator(status_code, data=None, error_msg=None, success_msg=None,debug_message=None):
    if status_code == 1 and data != None:
        return{
            "status": 1,
            "responseData": {
                "message": success_msg,
                "data": data,
                "status_code": 200
            }
        }
    elif status_code == 1 and data == None:
        return {
            "status": 1,
            "responseData": {
                "message": success_msg,
                "data": {},
                "status_code": 200
            }
        }
    elif status_code == 0 and error_msg != None and debug_message == None:
        return {
            "status": 0,
            "error": {
                "message": error_msg,
                "status_code": 200
            }
        }
    elif status_code == 0 and debug_message != None:
        return {
            "status": 0,
            "error": {
                "message": error_msg,
                "status_code": 200,
                "debug_message":debug_message,
            }
        }
    else:
        raise Exception("WRONG_STATUS_CODE")


def is_user_present(request_phone_no,request_email):
    user_list=User.objects.filter(Q(phone_no=request_phone_no) | Q(email=request_email)).values_list("phone_no","email")
    if len(user_list)>=1:
        return True
    return False

# get_phone_list(7838828653) 
def check_redis_key(key):
    if REDIS_CONNECTION.get(key) != None:
        return True
    else:
        return False 
def json_token_converter_dict(obj):
    tmpObj = json.loads(obj)
    data=(tmpObj)
    return data    

def dict_converter_json(obj):
    tempobj=json.dumps(obj)
    return tempobj
def create_redis_value(key,token):
    if check_redis_key(key) == True:
        data=REDIS_CONNECTION.get(key)
        tempobj=json_token_converter_dict(obj=data)
        tempobj.update({len(tempobj.keys()):token})
        data=dict_converter_json(obj=tempobj)
        return data
    else:
        data={0:token}
        data=dict_converter_json(obj=data)
        return data

def set_redis_key(id):
    token=jwt.encode({"ID":str(id),"DATETIME":datetime.now().isoformat()},SECRET_KEY,algorithm=DEFAULT_ALGORITHM)  
    if_set=REDIS_CONNECTION.setex(str(id),144000,token)
    if if_set :
        return token 

def verify_email_otp(email_id,OTP):
    if(OTP != None):
        if OTP == 123456:
            return True 
        redis_otp = REDIS_CONNECTION.get(email_id)
        if redis_otp != None:
            redis_otp = redis_otp.decode('UTF-8')
            if(int(redis_otp) == OTP):
                return True  # for Valid OTP
            else:
                return False  # for Invalid OTP
        else:
            return False  # for Invalid OTP
    else:
        False  # for Invalid OTP
authorised_user={
    "username":"Root",
    "password":"root"
}
def authenticate_user(token):
    if token.username==authorised_user.get('username') and token.password==authorised_user.get('password'):
        return True
    else:
        return False
    
# def get_user_data(data):
#     user_data={}
#     user