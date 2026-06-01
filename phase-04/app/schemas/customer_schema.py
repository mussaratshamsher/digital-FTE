from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, Any
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    lead_score: Optional[int] = 0
    lead_status: Optional[str] = "new"
    sentiment_health: Optional[str] = "Neutral"
    last_sentiment_score: Optional[int] = 50

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    lead_score: Optional[int] = None
    lead_status: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    
    # UI Compatibility Fields
    score: int = 0
    sentiment: str = "Neutral"
    last_activity: str = "N/A"
    value: str = "$0"
    industry: str = "General"

    @model_validator(mode='before')
    @classmethod
    def populate_ui_fields(cls, data: Any) -> Any:
        if hasattr(data, "lead_score"):
            # Use setattr because we can't directly assign to attributes of some objects in 'before' validator
            try:
                # Try setting attributes if it's a simple object
                data.score = data.lead_score or 0
                data.sentiment = data.sentiment_health or "Neutral"
                data.last_activity = data.created_at.strftime("%Y-%m-%d %H:%M") if data.created_at else "N/A"
                data.value = f"${(data.lead_score or 0) * 1000:,}"
                data.industry = data.company or "General"
            except:
                # If we can't set them (like on SQLAlchemy models), we'll return a dict instead
                base_dict = {c.name: getattr(data, c.name) for c in data.__table__.columns} if hasattr(data, '__table__') else (data.__dict__ if hasattr(data, '__dict__') else {})
                return {
                    **base_dict,
                    "score": getattr(data, "lead_score", 0) or 0,
                    "sentiment": getattr(data, "sentiment_health", "Neutral") or "Neutral",
                    "last_activity": data.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(data, "created_at") and data.created_at else "N/A",
                    "value": f"${(getattr(data, 'lead_score', 0) or 0) * 1000:,}",
                    "industry": getattr(data, "company", "General") or "General"
                }
        elif isinstance(data, dict):
            data["score"] = data.get("lead_score", 0) or 0
            data["sentiment"] = data.get("sentiment_health", "Neutral") or "Neutral"
            created_at = data.get("created_at")
            if isinstance(created_at, datetime):
                data["last_activity"] = created_at.strftime("%Y-%m-%d %H:%M")
            data["value"] = f"${(data.get('lead_score', 0) or 0) * 1000:,}"
            data["industry"] = data.get("company", "General") or "General"
        return data

    class Config:
        from_attributes = True
