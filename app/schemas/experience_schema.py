from pydantic import BaseModel, Field
from datetime import date

class ExperienceCreate(BaseModel):
    designation: str = Field(min_length=1)
    organization: str = Field(min_length=1)
    is_current: bool
    start: date
    end: date | None = None