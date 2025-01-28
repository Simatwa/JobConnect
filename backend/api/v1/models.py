from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class JobResponse(BaseModel):
    id: int
    company: str
    category: str
    title: str
    type: Literal["Full-time", "Internship"]
    min_salary: int
    max_salary: int
    updated_at: datetime


class JobsAvailable(BaseModel):

    total: int = Field(description="Total jobs available")
    jobs: list[JobResponse]


class JobDetails(BaseModel):
    details: Optional[JobResponse] = None
    description: str
