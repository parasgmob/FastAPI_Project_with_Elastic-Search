import redis
from decouple import config

REDIS_CONNECTION=redis.Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=0)

TWILIO_ACCOUNT_SID=config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN=config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NO=config('TWILIO_PHONE_NO')

SECRET_KEY=config('SECRET_KEY')
DEFAULT_ALGORITHM=config('DEFAULT_ALGORITHM')

    