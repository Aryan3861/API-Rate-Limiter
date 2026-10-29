from datetime import datetime
from sqlalchemy import Boolean, DateTime,Float, Integer,String, func
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base

class RequestLog(Base):
    tablename="request_logs"
    id: Mapped[int]=mapped_column(primary_key=True)
    request_id: Mapped[str] = mapped_column(String(50), index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    client_ip: Mapped[str] = mapped_column(String(64), index=True)
    method: Mapped[str] = mapped_column(String(10))
    endpoint: Mapped[str] = mapped_column(String(255), index=True)
    status_code: Mapped[int] = mapped_column(Integer)
    is_allowed: Mapped[bool] = mapped_column(Boolean)
    latency_ms: Mapped[float] = mapped_column(Float)