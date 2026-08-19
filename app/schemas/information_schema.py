from pydantic import BaseModel, EmailStr, Field

class Information(BaseModel):
    profile_summary: str=Field(min_length=1)
    email: EmailStr
    message: str=Field(min_length=1)
    skills: list[str]=Field(min_length=1)
    profile: str=Field(min_length=1)
    resume: str=Field(min_length=1)


class InformationUpdate(BaseModel):
    # text fields required, file-url fields optional (None = purani value rakho)
    profile_summary: str=Field(min_length=1)
    email: EmailStr
    message: str=Field(min_length=1)
    skills: list[str] | None = None
    profile: str | None = None
    resume: str | None = None