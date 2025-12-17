from pydantic import BaseModel, Field

class PreferenceRequest(BaseModel):
    preference: str = Field(..., description="User's natural language preferences")
