from pydantic import BaseModel, Field 

class ProjectCreate(BaseModel):
    project_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    tech_used: list[str] = Field(min_length=1)
    image_url: str = Field(min_length=1)
    live_link: str = Field(min_length=1)
    github_url: str = Field(min_length=1)


class ProjectUpdate(BaseModel):
    # image_url optional (None = purani image rakho), baaki text required
    project_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    tech_used: list[str] = Field(min_length=1)
    image_url: str | None = None
    live_link: str = Field(min_length=1)
    github_url: str = Field(min_length=1)
    