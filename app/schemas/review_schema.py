from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ReviewCreate(BaseModel):
    review_text: str = Field(..., min_length=30)
    rating: int = Field(..., ge=1, le=5)

class ReviewResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    review_text: str
    rating: int

    model_config = ConfigDict(from_attributes=True)
