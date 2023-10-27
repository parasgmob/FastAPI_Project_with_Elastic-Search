from mongoengine import *
from datetime import datetime

class Post(Document):
  user_id=ReferenceField('User',required=True)
  title=StringField(max_length=250)
  post_data=StringField()
  created_at=DateTimeField(default=datetime.now())
  updated_at=DateTimeField(default=datetime.now())


class Comment(Document):
  post_id=ReferenceField('Post',required=True,reverse_delete_rule=CASCADE)
  user_id=ReferenceField('User',required=True,reverse_delete_rule=CASCADE)
  content=StringField(max_length=250)
  reply_id=ReferenceField('self',reverse_delete_rule=CASCADE)
  created_at=DateTimeField(default=datetime.utcnow())
  updated_at=DateTimeField(default=datetime.utcnow())



