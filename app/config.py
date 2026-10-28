from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name:str="API Rate Limiter & Traffic Monitor"
    redis_url:str="redis://redis:6379/0"
    database_url:str="postgresql+asyncpg://postgres:postgres@db:5432/rate_limiter"
    
    rate_limit_requests:int=10
    rate_limit_window_seconds:int=60
    model_config=SettingsConfigDict(env_file=".env",extra="ignore",)
settings=Settings()
