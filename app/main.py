from app.schema import URL_Request, URL_Response
from app.model import save_url, retrieve_function
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.database import *
app = FastAPI()

# Shorten a long URL
@app.post("/shorten", response_model=URL_Response)
async def shorten_url(request: URL_Request):
    short_id = str(save_url(request.long_url))  # Pass the long_url string
    print(short_id)
    return URL_Response(short_url=f"http://localhost:8000/{short_id}")  # or use domain

# Retrieve and redirect to the original long URL
@app.get("/{short_url}")
async def retreival(short_url: str):
    long_url = retrieve_function(short_url)
    if not long_url:
        raise HTTPException(status_code=404, detail="Short URL cannot be found!")
    return {"long_url":long_url}

@app.get("/analytics/{short_url}")
async def get_analytics(short_url: str):
    count = cache.get(f"analytics:{short_url}")
    return {"short_url": short_url, "access_count": int(count) if count else 0}