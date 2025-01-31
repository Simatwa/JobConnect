"""Utilities fuctions for v1
"""

import uuid
import random
from string import ascii_lowercase
from api.v1.models import NewJob, UpdateJob
from jobs.models import JobCategory
from fastapi import HTTPException, status
from functools import wraps

token_id = "jbc_"


def generate_token() -> str:
    """Generates api token"""
    return token_id + str(uuid.uuid4()).replace("-", random.choice(ascii_lowercase))


def validate_category_id(func):
    """Decorator that ensures category_id specified actually exists"""

    @wraps(func)
    def decorator(job_details: NewJob | UpdateJob, **kwargs):
        try:
            if job_details.category_id is not None:
                JobCategory.objects.get(id=job_details.category_id)
            return func(job_details, **kwargs)
        except JobCategory.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Job category specified '{job_details.category_id}' does not exist.",
            )

    return decorator
