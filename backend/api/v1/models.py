from pydantic import BaseModel, Field, PositiveInt, field_validator
from typing import Literal, Optional, TypeAlias
from datetime import datetime
from jobs.models import JobCategory, Job

JobType: TypeAlias = Literal["Full-time", "Internship"]


class JobResponse(BaseModel):
    id: int
    company: str
    category: str
    title: str
    type: JobType
    min_salary: int
    max_salary: int
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "company": "Tech Innovators Inc.",
                "category": "Software Engineering",
                "title": "Senior Software Engineer",
                "type": "Full-time",
                "min_salary": 90000,
                "max_salary": 120000,
                "updated_at": "2023-10-01T12:00:00Z",
            }
        }
    }


class JobsAvailable(BaseModel):

    total: int = Field(description="Total jobs available")
    jobs: list[JobResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 1,
                "jobs": [
                    {
                        "id": 1,
                        "company": "Tech Innovators Inc.",
                        "category": "Software Engineering",
                        "title": "Senior Software Engineer",
                        "type": "Full-time",
                        "min_salary": 90000,
                        "max_salary": 120000,
                        "updated_at": "2023-10-01T12:00:00Z",
                    }
                ],
            }
        }
    }


class JobDetails(BaseModel):
    details: Optional[JobResponse] = None
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "details": {
                    "id": 1,
                    "company": "Tech Innovators Inc.",
                    "category": "Software Engineering",
                    "title": "Senior Software Engineer",
                    "type": "Full-time",
                    "min_salary": 90000,
                    "max_salary": 120000,
                    "updated_at": "2023-10-01T12:00:00Z",
                },
                "description": "This is a detailed job description for the Senior Software Engineer position.",
            }
        }
    }


class CategoriesAvailable(BaseModel):
    class Categories(BaseModel):
        id: int
        name: str
        description: str
        jobs_amount: int

    total: int = Field(description="Categories amount")
    categories: list[Categories]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 2,
                "categories": [
                    {
                        "id": 1,
                        "name": "Software Engineering",
                        "description": "Jobs related to software development and engineering.",
                        "jobs_amount": 150,
                    },
                    {
                        "id": 2,
                        "name": "Data Science",
                        "description": "Jobs related to data analysis and machine learning.",
                        "jobs_amount": 80,
                    },
                ],
            }
        }
    }


class TokenAuth(BaseModel):
    """
    - `access_token` : Token value.
    - `token_type` : bearer
    """

    access_token: str
    token_type: Optional[str] = "bearer"

    model_config = {
        "json_schema_extras": {
            "example": {
                "access_token": "jbc_27b9d79erc245r44b9rba2crd2273b5cbb71",
                "token_type": "bearer",
            }
        }
    }


class Feedback(BaseModel):
    detail: str = Field(description="Feedback in details")


class NewJob(BaseModel):
    category_id: int
    title: str
    type: JobType
    maximum_salary: PositiveInt
    minimum_salary: PositiveInt
    description: str
    is_available: bool = True

    @field_validator("category_id")
    def validate_category_id(value):
        try:
            JobCategory.objects.get(id=value)
            return value
        except JobCategory.DoesNotExist:
            raise ValueError("There is no job category with that id.")


class UpdateJob(NewJob):
    id: int
    category_id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[JobType] = None
    maximum_salary: Optional[PositiveInt] = None
    minimum_salary: Optional[PositiveInt] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None

    @field_validator("category_id")
    def validate_category_id(value):
        try:
            Job.objects.get(id=value)
            return value
        except JobCategory.DoesNotExist:
            raise ValueError("There is no job with that id.")
