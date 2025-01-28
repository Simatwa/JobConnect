from fastapi import APIRouter, Query
from typing import Annotated
from api.v1.models import JobsAvailable
from jobs.models import Job
from typing import Literal

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/jobs", name="Job listings")
def get_jobs_available(
    type: Annotated[
        Literal["Internship", "Full-time", "All"],
        Query(description="Job type either `Intership` or `Full-time`"),
    ] = "All",
    category: Annotated[
        str, Query(description="Category title to serve as filter")
    ] = None,
    offset: Annotated[int, Query(description="Jobs available offset value")] = None,
    limit: Annotated[
        int, Query(description="Number of jobs not to exceed", ge=5, le=100)
    ] = 20,
) -> JobsAvailable:
    """Get jobs available"""
    filter = []
    if type and type != "All":
        filter.append(type__exact=type)
    if category:
        filter.append(category_title__exact=category)
    objects: list[Job] = Job.objects.filter(*filter).all()
    if offset and len(objects) > offset:
        objects = objects[:offset]
    jobs_found = []
    for job in objects:
        jobs_found.append(
            dict(
                company=job.company.__str__(),
                category=job.category.name,
                title=job.title,
                type=job.type,
                min_salary=job.minimum_salary,
                max_salary=job.maximum_salary,
                updated_at=job.updated_at,
            )
        )

    return JobsAvailable(total=len(objects), jobs=jobs_found)
