from mongoengine import *

connect(db='testdb', host='localhost', port=27017)


# mongoehgine doc https://mongoengine-odm.readthedocs.io/guide/connecting.html

class testcolletion(DynamicDocument):  # for making dynamic collection you can use any no of field 
  meta = {'collection': 'testcollection'}  # using existing collection from db
  
