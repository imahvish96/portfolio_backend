from pydantic import BaseModel, EmailStr, Field
from datetime import date

class ExperienceCreate(BaseModel):
    designation: str=Field(min_length=1)
    organization: str = Field(min_length=1)
    start: date
    end: date