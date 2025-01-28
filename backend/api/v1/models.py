from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class JobsAvailable(BaseModel):
    class Jobs(BaseModel):
        company: str
        category: Optional[str] = None
        title: str
        type: Literal["Full-time", "Internship"]
        min_salary: int
        max_salary: int
        updated_at: datetime

    total: int = Field(description="Total jobs available")
    jobs: list[Jobs]
