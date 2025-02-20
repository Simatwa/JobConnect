from pydantic import BaseModel, Field, PositiveInt, EmailStr, field_validator
from typing import Literal, Optional, TypeAlias
from datetime import datetime, date
from django.templatetags.static import static
from django.conf import settings
import os

JobType: TypeAlias = Literal["Full-time", "Internship"]


class JobResponse(BaseModel):
    id: int
    company_id: int
    company_username: str
    category_id: int
    category_name: str
    title: str
    type: JobType
    min_salary: int
    max_salary: int
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "company_id": 1,
                "company_username": "Tech Innovators Inc.",
                "category_id": 1,
                "category_name": "Software Engineering",
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
                "total": 2,
                "jobs": [
                    {
                        "id": 1,
                        "company_id": 1,
                        "company_username": "Tech Innovators Inc.",
                        "category_id": 1,
                        "category_name": "Software Engineering",
                        "title": "Senior Software Engineer",
                        "type": "Full-time",
                        "min_salary": 90000,
                        "max_salary": 120000,
                        "updated_at": "2023-10-01T12:00:00Z",
                    },
                    {
                        "id": 2,
                        "company_id": 2,
                        "company_username": "Data Wizards LLC",
                        "category_id": 2,
                        "category_name": "Data Science",
                        "title": "Data Analyst",
                        "type": "Full-time",
                        "min_salary": 70000,
                        "max_salary": 90000,
                        "updated_at": "2023-10-02T12:00:00Z",
                    },
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
                    "company_id": 1,
                    "company_username": "Tech Innovators Inc.",
                    "category_id": 1,
                    "category_name": "Software Engineering",
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


class CategoryInfo(BaseModel):
    id: int
    name: str
    description: str
    jobs_amount: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Software Engineering",
                "description": "Jobs related to software development and engineering.",
                "jobs_amount": 150,
            }
        }
    }


class CategoriesAvailable(BaseModel):
    total: int = Field(description="Categories amount")
    categories: list[CategoryInfo]

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

    model_config = {
        "json_schema_extra": {
            "example": {"detail": "This is a detailed feedback message."}
        }
    }


class NewJob(BaseModel):
    category_id: int
    title: str
    type: JobType
    max_salary: PositiveInt
    min_salary: PositiveInt
    description: str
    is_available: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "category_id": 1,
                "title": "Senior Software Engineer",
                "type": "Full-time",
                "max_salary": 120000,
                "min_salary": 90000,
                "description": "This is a detailed job description for the Senior Software Engineer position.",
                "is_available": True,
            }
        }
    }


class UpdateJob(NewJob):
    id: int
    category_id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[JobType] = None
    max_salary: Optional[PositiveInt] = None
    min_salary: Optional[PositiveInt] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "category_id": 2,
                "title": "Junior Data Scientist",
                "type": "Internship",
                "max_salary": 60000,
                "min_salary": 40000,
                "description": "This is a detailed job description for the Junior Data Scientist position.",
                "is_available": True,
            }
        }
    }


class CompanyDetails(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    location: Optional[str] = None
    category: Literal["Organization", "Individual"]
    description: Optional[str] = None
    profile: Optional[str] = None

    model_config = {
        "json_schema_extras": {
            "example": {
                "id": 1,
                "username": "EvilCorp",
                "first_name": "EvilCorp LLC",
                "last_name": "",
                "email": "cynthiaholloway@example.net",
                "phone_number": "001-807-204-9641",
                "location": "3947 Wall Shoals\nAaronland, DE 03034",
                "category": "Individual",
                "description": None,
                "profile": "/static/default/user_avatar.png",
            }
        }
    }

    @field_validator("profile")
    def validate_profile(value):
        if bool(value):
            return static(value)
        else:
            return None


class CompleteApplicantDetails(CompanyDetails):
    gender: Literal["Male", "Female", "Other"]
    dob: Optional[date] = Field(description="Date of birth")
    document: Optional[str] = Field(
        description="Applicant resume or CV", alias="documents"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "123-456-7890",
                "location": "123 Main St, Anytown, USA",
                "category": "Individual",
                "description": "Experienced software developer",
                "profile": "/static/default/user_avatar.png",
                "gender": "Male",
                "dob": "1990-01-01",
                "document": "/media/resumes/john_doe_resume.pdf",
            }
        }
    }

    @field_validator("document")
    def validate_document(value):
        if bool(value):
            return os.path.join("/", settings.MEDIA_URL, value)
        else:
            return None


class JobApplicants(BaseModel):
    total: int = Field(description="Job applicants amount")
    applicants: list[CompleteApplicantDetails]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 2,
                "applicants": [
                    {
                        "id": 1,
                        "username": "john_doe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "123-456-7890",
                        "location": "123 Main St, Anytown, USA",
                        "category": "Individual",
                        "description": "Experienced software developer",
                        "profile": "/static/default/user_avatar.png",
                        "gender": "Male",
                        "dob": "1990-01-01",
                        "document": "/media/resumes/john_doe_resume.pdf",
                    },
                    {
                        "id": 2,
                        "username": "jane_smith",
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "email": "jane.smith@example.com",
                        "phone_number": "987-654-3210",
                        "location": "456 Elm St, Othertown, USA",
                        "category": "Individual",
                        "description": "Data scientist with 5 years of experience",
                        "profile": "/static/default/user_avatar.png",
                        "gender": "Female",
                        "dob": "1985-05-15",
                        "document": "/media/resumes/jane_smith_resume.pdf",
                    },
                ],
            }
        }
    }
