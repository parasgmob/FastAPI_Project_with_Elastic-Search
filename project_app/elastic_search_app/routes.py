from fastapi import APIRouter,Body
from .db_config import *
from .client import es

elastic_search=APIRouter(tags=["elastic search"])

async def get_document():
  el_obj=testcolletion.objects()
  for i in el_obj:
    inside_dict={}
    inside_dict["first_name"]=i.first_name
    inside_dict["last_name"]=i.last_name
    inside_dict["job_title"]=i.job_title
    inside_dict["email"]=i.email
    inside_dict["company"]=i.company
    inside_dict["city"]=i.city
    resp = es.index(index="test-index", id=i.id, document=inside_dict)
  return("success")
  
# resp = es.index(index="test-index", id="63d10371b65953cbad6da04b", document={"first_name":"Paras","last_name":"Gupta","job_title":"Python Developer","email":"paras123@gmail.com","company":"Mobcoder","city":"Noida"})
# print(resp)

@elastic_search.get("/search")
async def search_document(search_text:str):
  q={
    "bool": {
      "must": [
        {
          "query_string": {
            "fields": ["first_name","city","job_title","last_name","company"],
            "query":search_text+str('*')
          }
        }
      ]
       }
    }
  search_obj=es.search(index="test-index", query=q,size=100) #{"match_all":{}}
  return (search_obj,"sdssssssss")

@elastic_search.get("/search/id/")
async def search_by_id(search_id:str):
  search_obj=es.get(index="test-index",id=search_id)
  return search_obj

@elastic_search.post("/update/")
async def update_document(search_id:str,first_name1:str=Body()):
  search_obj=es.update(index="test-index",id=search_id,body={"doc":{"first_name":first_name1}})
  return search_obj















# @elastic_search.post("/analyze/")
# async def analyze_document():
#   search_obj=es.analyze(
#     body={
#         "tokenizer": "standard",
#   "text": "I'm in the mood for drinking semi-dry red wine!"
#     }
# )

#   return search_obj


#  curl -XGET "http://localhost:9200/test-index/_analyze"?pretty -H 'Content-Type: application/json' -d'
# {
#   "analyzer": "standard",
#   "text": "jestem biały miś"
# }'