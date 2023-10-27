from random           import randrange
from twilio.rest      import Client
from message          import TWILIO_MESSAGE
from celery           import Celery, shared_task
from fastapi_mail     import FastMail, MessageSchema,ConnectionConfig
from configurations   import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_PHONE_NO,REDIS_CONNECTION

conf = ConnectionConfig(
    MAIL_USERNAME="mahendra.chaurasiya@mobcoder.com",
    MAIL_PASSWORD="M9810232935",
    MAIL_FROM="mahendra.chaurasiya@mobcoder.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_mail(request_mail):
   try:
        OTP = str(randrange(100000, 999999))
        template = "Email verification "+OTP
        message = MessageSchema(
            subject="email verificaton",
            recipients=[request_mail],  
            body=template,
            subtype="html"
            )
    
        fm = FastMail(conf)
        await fm.send_message(message)
        REDIS_CONNECTION.setex(request_mail, 60*10, OTP)
   except Exception as e:
       print(e)


async def send_phone_verification(send_to, country_code):
    if type(send_to) == type(int()):
        send_to = str(send_to)
    send_to = '+' + str(country_code) + str(send_to)
    OTP = str(randrange(100000, 999999))
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twilio_client.messages.create(
        body=TWILIO_MESSAGE+str(OTP), from_=TWILIO_PHONE_NO, to=[send_to])
    print('phone otp',OTP)
    REDIS_CONNECTION.setex(send_to.casefold(), 60*10, OTP)
    return 'DONE'
