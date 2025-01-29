from fastapi import APIRouter, Query, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from api.v1.models import (
    JobsAvailable,
    JobDetails,
    CategoriesAvailable,
    TokenAuth,
    Feedback,
    NewJob,
    UpdateJob,
)
from jobs.models import Job, JobCategory
from users.models import CustomUser
from django.contrib.auth.hashers import check_password, make_password
from typing import Literal
from api.v1.utils import form_job_details, generate_token, token_id
import asyncio

router = APIRouter(prefix="/v1", tags=["v1"])

v1_auth_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token",
    description="Generated API authentication token",
)


async def get_user(token: Annotated[str, Depends(v1_auth_scheme)]) -> CustomUser:
    """Ensures token passed match the one set"""
    if token:
        try:
            if token.startswith(token_id):

                def fetch_user(token):
                    return CustomUser.objects.get(token=token)

                return await asyncio.to_thread(fetch_user, token)

        except CustomUser.DoesNotExist:
            pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token")
def fetch_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenAuth:
    """
    - `username` : User email.
    - `password` : User password.
    """
    try:
        user = CustomUser.objects.get(email=form_data.username)
        if check_password(form_data.password, user.password):
            if user.token is None:
                user.token = generate_token()
                user.save()
            return TokenAuth(access_token=user.token, token_type="bearer")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )
    except CustomUser.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
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
    user_id: Annotated[
        int, Query(description="Return jobs posted by user identified by this id")
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

    if user_id:
        filter["id"] = id

    objects: list[Job] = Job.objects.filter(**filter).all()
    if offset and len(objects) > offset:
        objects = objects[:offset]
    jobs_found = []
    for count, job in enumerate(objects, start=1):
        jobs_found.append(form_job_details(job))
        if count == limit:
            break

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


@router.post(
    "/job",
    name="Add new job",
)
def add_new_job(
    new_job: NewJob, user: Annotated[CustomUser, Depends(get_user)]
) -> Feedback:
    """Make new job entry"""
    Job.objects.create(
        company=user,
        category=JobCategory.objects.get(id=new_job.category_id),
        title=new_job.title,
        type=new_job.type,
        minimum_salary=new_job.minimum_salary,
        maximum_salary=new_job.maximum_salary,
        description=new_job.description,
        is_available=new_job.is_available,
    ).save()
    return Feedback(detail="New job created successfully")


@router.patch("/job", name="Update existing job")
def update_existing_job(
    job_details: UpdateJob, user: Annotated[CustomUser, Depends(get_user)]
) -> Feedback:
    """Modify existing job"""
    get_value: lambda old, new: new or old
    try:
        target_job = Job.objects.get(id=job_details.id, company=user)
        if job_details.category_id:
            target_job.category = JobCategory.objects.get(id=job_details.category_id)
        target_job.title = get_value(target_job.title, job_details.title)
        target_job.type = get_value(target_job.type, job_details.type)
        target_job.maximum_salary = get_value(
            target_job.maximum_salary, job_details.maximum_salary
        )
        target_job.minimum_salary = get_value(
            target_job.minimum_salary, job_details.minimum_salary
        )
        target_job.description = get_value(
            target_job.description, job_details.description
        )
        target_job.is_available = get_value(
            target_job.is_available, job_details.is_available
        )
        target_job.save()
    except Job.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only update a job that you created.",
        )


@router.delete("/job/{id}", name="Delete a job")
def delete_existing_job(
    id: int, user: Annotated[CustomUser, Depends(get_user)]
) -> Feedback:
    """Delete an existing job"""
    try:
        target_job = Job.objects.get(id=id)
        if target_job.company.id == user.id:
            target_job.delete()
            return Feedback(detail="Job deleted successfuly.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete a job that you posted.",
        )
    except Job.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id '{id}' does not exist.",
        )
