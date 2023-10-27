from utility import *
from .models import *
from .schemas import *
from fastapi import APIRouter,Request
from datetime import datetime
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import FastAPI,status, File, UploadFile,Depends
from . import service

auth_scheme = HTTPBearer(scheme_name='token')
async def verify_token(token: str = Depends(auth_scheme)):
    return token

post=APIRouter(
    tags=['post'],dependencies=[Depends(verify_token)]
)

@post.get("/all/post")
async def get_all_post(token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            uk_users =Post.objects(user_id=user_id)
            post_list=[]
            for i in uk_users:
                inside_dict={}
                inside_dict["id"]=str(i.id)
                inside_dict["title"]=i.title
                inside_dict["post_data"]=i.post_data
                post_list.append(inside_dict)
            success_response_dict["post"]=post_list
            return JSONResponse(success_response_dict)
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except Exception as e:
        return JSONResponse({"msg":"Unsuccess"+" "+str(e),"status_code":200})

@post.get("/post/")
async def get_post(post_id:str,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            uk_users =Post.objects(id=post_id)
            post_list=[]
            for i in uk_users:
                inside_dict={}
                inside_dict["id"]=str(i.id)
                inside_dict["title"]=i.title
                inside_dict["post_data"]=i.post_data
                inside_dict["created_at"]=i.created_at
                inside_dict["updated_at"]=i.updated_at
                post_list.append(inside_dict)
            success_response_dict["post"]=post_list
            return success_response_dict
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except:
        return JSONResponse({"msg":"Unsuccess","status_code":200})

@post.post("/uploadfile/")
async def create_post(data:Create_Post_Schema=Depends(Create_Post_Schema.as_form),post_data:Union[UploadFile,None]=File(default=None),token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            post_obj=Post(user_id=user_id,title=data.title)
            file_loc="/home/mobcoder/Desktop/fastapi-social/fastapi-socialapp/app/media/"+str(post_data.filename)
            with open(file_loc ,"wb") as ufile:
                ufile.write(post_data.file.read())
            post_obj.post_data=file_loc
            post_obj = post_obj.save()
            return {"msg":"Success","status_code":200}
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except Exception as e:
        return JSONResponse({"msg":"Unsuccess"+" "+str(e),"status_code":200})

@post.patch("/update/post")
async def update_post(post_id:str,data:Update_Post_Schema=Depends(Update_Post_Schema.as_form),post_data:Union[UploadFile,None]=File(default=None),token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            if data.title!=None and post_data!=None:
                file_loc="/home/mobcoder/Desktop/fastapi-social/fastapi-socialapp/app/media/"+str(post_data.filename)
                with open(file_loc ,"wb") as ufile:
                    ufile.write(post_data.file.read())
                Post.objects(id=post_id).update(title=data.title,post_data=file_loc)
                return JSONResponse({"msg":"success","status_code":200})
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except:
        return JSONResponse({"msg":"Unsuccess","status_code":200})

@post.delete("/delete/post")
async def delete_post(post_id:str,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            Post.objects(id=post_id).delete()
            return JSONResponse({"msg":"success","status_code":200})
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except:
        return JSONResponse({"msg":"Unsuccess","status_code":200})

@post.get("/all/comment")
async def get_all_comment(post_id:str,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            comment_obj =Comment.objects(post_id=post_id)
            comment_dict={"msg":"Success","status_code":200}
            comment_list=[]
            for i in comment_obj:
                inside_dict={}
                inside_dict["post_id"]=str(i.post_id.id)
                #inside_dict["user_id"]=str(i.user_id)
                inside_dict["content"]=i.content
                inside_dict["reply_id"]=i.reply_id
                comment_list.append(inside_dict)
            comment_dict["post"]=comment_list
            return JSONResponse(comment_dict)
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except Exception as e:
        return JSONResponse({"msg":"Unsuccess"+" "+str(e),"status_code":200})

@post.post("/create/comment")
async def create_comment(comment_data:Create_Comment_Schema,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            comment_obj=Comment(post_id=comment_data.post_id,user_id=comment_data.user_id,content=comment_data.content,reply_id=comment_data.reply_id)
            post_obj = comment_obj.save()
            return JSONResponse("Success")
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except:
        return JSONResponse({"msg":"Unsuccess","status_code":200}) 

@post.delete("/delete/comment")
async def delete_comment(comment_id:str,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            Comment.objects(id=comment_id).delete()
            return JSONResponse({"msg":"success","status_code":200})
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except Exception as e:
        return JSONResponse({"msg":"Unsuccess"+" "+str(e),"status_code":200})
     

@post.patch("/update/comment")
async def update_comment(comment_id:str,data:Update_Comment_Schema,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            Comment.objects(id=comment_id).update(content=data.content)
            return JSONResponse({"msg":"success","status_code":200})
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except:
        return JSONResponse({"msg":"Unsuccess","status_code":200})

@post.post("/create/comment/reply")
async def create_reply(comment_id:str,reply_content:Create_Reply_Comment_Schema,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:
            comment_obj=Comment(reply_id=comment_id,user_id=reply_content.user_id,post_id=reply_content.post_id,content=reply_content.content)
            comment_obj.save()
            return JSONResponse("Success")
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except Exception as e:
        return JSONResponse({"msg":"Unsuccess"+" "+str(e),"status_code":200})

@post.get("/comment/reply",status_code=200,description="Getting reply on a comment")
async def get_comment_reply(comment_id:str,token=Depends(auth_scheme)):
    try:
        session_result,user_id=check_session(token.credentials,return_Id=True)
        if session_result:

            reply_obj=Comment.objects(reply_id=comment_id)
            list1=[]
            for i in reply_obj:
                inside_dict={}
                inside_dict["id"]=str(i.id)
                # inside_dict["post_id"]=str(i.post_id.id)
                inside_dict["user_id"]=str(i.user_id.id)
                inside_dict["content"]=i.content
                inside_dict["reply_id"]=i.reply_id
                list1.append(inside_dict)

                
            pipeline=[{"$lookup":{"from":'user',"localField":"user_id","foreignField":"_id","as":"comments"}}]
            ne=Comment.objects().aggregate(pipeline)
            for i in ne:
                print(i,"iii")
            return ({"msg":"Success","data":list1,"status_code":200})
        else:
            return JSONResponse({"msg":"User not login","status_code":200})
    except Exception as e:
        return JSONResponse({"msg":"Unsuccess"+" "+str(e),"status_code":200})


