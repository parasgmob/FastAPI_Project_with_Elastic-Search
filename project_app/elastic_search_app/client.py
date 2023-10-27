from elasticsearch import Elasticsearch

es=Elasticsearch(hosts=["http://127.0.0.1:9200"]) #[{"host":"localhost","port":9200}]

# print(es.info(),"info") #You can all information about elasticesearch cluster
# print(es.ping(),"ping") # checking status of python client is connected to es or not

#es.indices.create(index="elasticsearchtut") #creating index


































sample_doc={"id":"63bba23320b4b978aad998fd","user_id":"63b420d711371bbc0fe0dbef","content":"reply he","reply_id":"63bad960dc8d3395923f01ce"
,"created_at":"2023-01-09T05:12:14.620+00:00","updated_at":"2023-01-09T05:12:14.620+00:00"
}

#p1=es.index(index="new",id=3,document=sample_doc) #If index is already exist then it will add data in that otherwise it will create new index

# total_indices=es.indices.get(index="*") # get all indexes
# for i in total_indices:
#   print(i)  #total_indices)

# check_index=es.search(index="test-index")
# print(check_index,"check_index")

# delete_indices=es.indices.delete(index="test-index")
# print(delete_indices,"delete_indices")


# import requests
# create_index=requests.put("http://localhost:9200/index_name")


# resp = es.index(index="test-index", id=1, document=doc)

# doc2={"id":"63bba23320b4b978aad998fd","user_id":"63b420d711371bbc0fe0dbef","content":"reply he he","reply_id":"63bad960dc8d3395923f01ce"
# ,"created_at":"2023-01-09T05:12:14.620+00:00","updated_at":"2023-01-09T05:12:14.620+00:00"
# }
# resp = es.index(index="test-index", id=2, document=doc2)

# doc3={"id":"63bba23320b4b978aad998fd","user_id":"63b420d711371bbc0fe0dbef","content":"reply he he he","reply_id":"63bad960dc8d3395923f01ce"
# ,"created_at":"2023-01-09T05:12:14.620+00:00","updated_at":"2023-01-09T05:12:14.620+00:00"
# }
# resp = es.index(index="test-index", id=3, document=doc3)
# print(resp['result'])

# doc4={"id":"63bba23320b4b978aad998fd","user_id":"63b420d711371bbc0fe0dbef","content":"reply he he he","reply_id":"63bad960dc8d3395923f01ce"
# ,"created_at":"2023-01-09T05:12:14.620+00:00","updated_at":"2023-01-09T05:12:14.620+00:00","mera-field":"paras gupta"
# }
# resp = es.index(index="test-index", id=4, document=doc4)
# # print(es.get(index="test-index",id=1))

# doc5={"id":"63bba23320b4b978aad998fd","user_id":"63b420d711371bbc0fe0dbef","content":"reply he he he","reply_id":"63bad960dc8d3395923f01ce"
# ,"created_at":"2023-01-09T05:12:14.620+00:00","updated_at":"2023-01-09T05:12:14.620+00:00","mera-field":"parasgsgsssssgs gupta"
# }
# resp = es.index(index="test-index", id=5, document=doc5)

# doc6={"id":"63bba23320b4b978aad998fd","user_id":"63b420d711371bbc0fe0dbef","content":"reply he he he","reply_id":"63bad960dc8d3395923f01ce"
# ,"created_at":"2023-01-09T05:12:14.620+00:00","updated_at":"2023-01-09T05:12:14.620+00:00","mera-field":"ssssssparasgsgsssssgs gupta"
# }
# resp = es.index(index="test-index", id=6, document=doc6)

# print(es.delete(index="test-index",id=1))

# print("ruunnn")
# print(es.get(index="test-index",id=1),"afterrrr")

# print(es.search(index="test-index"))

