from fastapi import FastAPI
from app.config import settings

app=FastAPI(title=settings.app_name,version="1.2.0")

@app.get("/")
def home():
    return {"message":"API is running"}
@app.get("/health")
async def health_check():
    return {"status":"ok",
            "service":settings.app_name }
