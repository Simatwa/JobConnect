"""Utilities fuctions for v1
"""

import uuid
import random
from string import ascii_lowercase
from api.v1.models import JobResponse
from jobs.models import Job

token_id = "jbc_"


def form_job_details(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        company=job.company.__str__(),
        category=job.category.name,
        title=job.title,
        type=job.type,
        min_salary=job.minimum_salary,
        max_salary=job.maximum_salary,
        updated_at=job.updated_at,
    )


def generate_token() -> str:
    return token_id + str(uuid.uuid4()).replace("-", random.choice(ascii_lowercase))
