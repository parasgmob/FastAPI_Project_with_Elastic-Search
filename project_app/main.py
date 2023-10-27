import time
from User.routes                    import user
from post.routes                    import post
from elasticsearch1.routes          import elastic_search
from decouple                       import config
from fastapi                        import FastAPI,Request,HTTPException
from mongoengine                    import connect,disconnect
from message                        import TOKEN_NOT_AVAILABLE
from fastapi.middleware.trustedhost import TrustedHostMiddleware

import logging
import random
import string

logging.config.fileConfig('logging.conf',disable_existing_loggers=False)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)


## run using uvicorn main:app --reload a
## want to chnage port  uvicorn main:app --port 9000 --reload

disconnect()
connect(config('db_name'), host=config('db_host'), port=27017)

app=FastAPI(title="CRUD with FastAPI", description= "Using Mongodb", version = "0.1.1")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if 'token' in dict(request.headers).keys():
        if request.headers.get('token')==None:
           raise HTTPException(TOKEN_NOT_AVAILABLE)
        else:
            pass
    response = await call_next(request)    
    return response
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

logging.basicConfig(filename="logging.log",level=logging.DEBUG)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.debug(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    return response

app.include_router(user)
app.include_router(post)
app.include_router(elastic_search)


from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


#customizing swaager ui

# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         title=app.title,
#         description=app.description,
#         version=app.version)
#         # oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         # swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
#         # swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css")