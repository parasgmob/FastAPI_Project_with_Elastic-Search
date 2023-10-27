from mongoengine import Document,StringField,EmailField,IntField,ImageField,BooleanField,DateTimeField
from mongoengine import connect
from mongoengine import Document,StringField,EmailField,IntField,ImageField,BooleanField
from datetime import datetime


class User(Document):
    full_name        =   StringField(max_length=50)
    email             =   EmailField(unique=True ,required=True)
    phone_no          =   IntField(unique=True,required=True)
    bio               =   StringField(max_length=255)
    profile_photo     =   ImageField()
    country_code      =   IntField(required=True)
    is_active         =   BooleanField(default=False)
    GENDER_CHOICES    =   (('male', 'male'),
                          ('female', 'female'),
                          ('other','other'))
    gender            =   StringField(max_length=10,choices=GENDER_CHOICES)
    password          =   StringField(min_length=9,max_length=15,required=True)
    
    created_at        =   DateTimeField(default=datetime.utcnow())
    updated_at        =   DateTimeField(auto_now=True)
    is_phone_verified =   BooleanField(default=True,null=False)
    is_email_verified =   BooleanField(default=False,null=False)

# obj=User(full_name="Paras Gupta")
# obj.save()

