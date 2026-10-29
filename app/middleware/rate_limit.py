import time
import uuid
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.rate_limit_scripts import SLIDING_WINDOW_SCRIPT

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self,app,redis_getter,limit:int,window_seconds: int):
        super().__init__(app)
        self.redis_getter=redis_getter
        self.limit=limit
        self.window_seconds=window_seconds

    async def dispatch(self,request:Request,call_next):
        if request.url.path in ["/health","/docs","/openapi.json","/metrics"]:
            return await call_next(request)

        redis=self.redis_getter()
        client_ip=self.get_client_ip(request)
        key=f"rate_limit:ip:{client_ip}"

        now_ms=int(time.time()*1000)
        window_ms=self.window_seconds*1000
        request_id=str(uuid.uuid4())
        allowed,used,limit=await redis.eval(SLIDING_WINDOW_SCRIPT,1,key,now_ms,window_ms,self.limit,request_id)

        remaining=max(limit-used,0)
        headers = {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(remaining),
        }


        if not allowed:
            headers["Retry-After"]=str(self.windoe_seconds)
            return JSONResponse(
                status_code=429,
                content={
                    "detail":"Too many requests. Please try again later.",
                    "limit":limit,
                    "used":used,
                    "remaining":remaining,
                },
                headers=headers,
            )
        
        response = await call_next(request)
        for key_name, value in headers.items():
            response.headers[key_name]=value
        return response

    def get_client_ip(self,request:Request)->str:
        forwarded_for=request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        return request.client.host if request.client else "unknown"