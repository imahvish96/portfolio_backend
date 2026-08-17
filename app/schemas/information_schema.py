from pydantic import BaseModel, EmailStr, Field

class Information(BaseModel):
    profile_summary: str=Field(min_length=1)
    email: EmailStr
    message: str=Field(min_length=1)
    skills: list[str]=Field(min_length=1)
    profile: str=Field(min_length=1)
    resume: str=Field(min_length=1)