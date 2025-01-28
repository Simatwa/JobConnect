from fastapi import APIRouter, Query, status, HTTPException
from typing import Annotated
from api.v1.models import JobsAvailable, JobDetails, JobResponse, CategoriesAvailable
from jobs.models import Job, JobCategory
from typing import Literal

router = APIRouter(prefix="/v1", tags=["v1"])


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
        int, Query(description="Number of jobs not to exceed", ge=1, le=100)
    ] = 20,
) -> JobsAvailable:
    """Get jobs available"""
    filter = {}
    if type and type != "All":
        filter["type__exact"] = type
    if category:
        filter["category__name__exact"] = category

    objects: list[Job] = Job.objects.filter(**filter).all()
    if offset and len(objects) > offset:
        objects = objects[:offset]
    jobs_found = []
    for job in objects:
        jobs_found.append(form_job_details(job))

    return JobsAvailable(total=len(objects), jobs=jobs_found)


@router.get("/job/{id}", name="Get job by ID")
def get_job_by_id(
    id: int,
    all: Annotated[
        bool, Query(description="Return all job details instead of just description")
    ] = False,
) -> JobDetails:
    """Get job details by ID"""
    target_job = Job.objects.filter(id=id).get()
    if target_job:
        if all:
            return JobDetails(
                details=form_job_details(target_job), description=target_job.description
            )
        else:
            return JobDetails(description=target_job.description)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No job found with id {id}")


@router.get("/categories")
def get_categories_available(
    limit: Annotated[
        int, Query(description="Categories amount not to exceed", ge=1, le=100)
    ] = 50
) -> CategoriesAvailable:
    """Explore categories available"""
    categories = JobCategory.objects.all()

    category_items = []

    for count, category in enumerate(categories, start=1):
        category_items.append(
            dict(
                id=category.id,
                name=category.name,
                description=category.description,
                jobs_amount=Job.objects.filter(category=category).count(),
            )
        )
        if count == limit:
            break
    return CategoriesAvailable(total=len(category_items), categories=category_items)
