import re
from message import *

def valid_name(name):
    if name.replace(" ","").isalpha()==False:
        raise ValueError(INVALID_NAME)
    return name


def valid_phone_no(phone):
    if len(str(phone))!=10:
        raise ValueError(INVALID_PHONE_NO)
    return phone


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email)==False:  
        raise ValueError(INVALID_EMAIL)
    return email.casefold()

def valid_password(pwd):
    special_characters = "!@#$%^&*()-+?_=,<>/"
    if(len(pwd) < 8):
        raise ValueError(INVALID_PASSWORD_LENGTH)
    flag1 = flag2 = flag3 = flag4 = False
    for x in pwd:
        if x.isupper():
            flag1 = True
        elif x.islower():
            flag2 = True
        elif x.isnumeric():
            flag3 = True
        elif x in special_characters:
            flag4 = True 
    if  (flag1 == False):
        raise ValueError("Error' use upercase character")
    elif(flag2 == False):
        raise ValueError("Error' use lowerercase character")
    elif(flag3 == False):
        raise ValueError("Error' use number character")
    elif(flag4 == False):
        raise ValueError("Error' use special character")
    else:
        return pwd


def valid_country_code(code):
    if len(str(code))>2:
        raise ValueError("Invalid country code")
    return code
    

def valid_gender(gender):
    print("ddddddddddddddddddd")
    return gender._value_
    # return gender.value()