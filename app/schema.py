from pydantic import BaseModel,HttpUrl

class URL_Request(BaseModel):
    long_url:HttpUrl
class URL_Response(BaseModel):
    short_url: HttpUrl