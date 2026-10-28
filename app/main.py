from fastapi import FastAPI
from app.config import settings
from contextlib import asynccontextmanager
from app.core.redis import close_redis,init_redis,get_redis
from app.middleware.rate_limit import RateLimitMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_redis()
    yield
    await close_redis()

app=FastAPI(title=settings.app_name,version="1.2.0",lifespan=lifespan)

app.add_middleware(
    RateLimitMiddleware,
    redis_getter=get_redis,
    limit=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)
@app.get("/")
def home():
    return {"message":"API is running"}

@app.get("/health")
async def health_check():
    return {"status":"ok",
            "service":settings.app_name }

@app.get("/api/test")
async def test_api():
    return {"message":"requests allowed"}
