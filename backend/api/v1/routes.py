from fastapi import APIRouter, Query, status, HTTPException, Depends, Path
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Literal
from api.v1.models import (
    JobsAvailable,
    JobDetails,
    CategoriesAvailable,
    TokenAuth,
    Feedback,
    NewJob,
    UpdateJob,
    JobResponse,
    CategoryInfo,
    CompanyDetails,
    CompleteApplicantDetails,
    JobApplicants,
)
from api.v1.utils import generate_token, token_id, validate_category_id
from jobs.models import Job, JobCategory
from users.models import CustomUser
from django.contrib.auth.hashers import check_password
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


@router.post("/token", name="User token")
def fetch_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenAuth:
    """
    - `username` : User username
    - `password` : User password.
    """
    try:
        user = CustomUser.objects.get(username=form_data.username)
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


@router.patch("/token", name="Generate new token")
def generate_new_token(user: Annotated[CustomUser, Depends(get_user)]) -> TokenAuth:
    user.token = generate_token()
    user.save()
    return TokenAuth(access_token=user.token)


@router.get("/jobs", name="Job listings")
def get_jobs_available(
    type: Annotated[
        Literal["Internship", "Full-time", "All"],
        Query(description="Job type either `Intership` or `Full-time`"),
    ] = "All",
    category_id: Annotated[
        int, Query(description="Fetch jobs with this category id")
    ] = None,
    user_id: Annotated[
        int, Query(description="Return jobs posted by user identified by this id")
    ] = None,
    start: Annotated[
        int, Query(description="Fetch jobs with id greater than this")
    ] = -1,
    offset: Annotated[int, Query(description="Jobs available offset value")] = None,
    limit: Annotated[
        int, Query(description="Number of jobs not to exceed", ge=1, le=100)
    ] = 20,
) -> JobsAvailable:
    """Get jobs available"""
    filter = {"is_available": True, "id__gt": start}
    if type and type != "All":
        filter["type__exact"] = type
    if category_id is not None:
        filter["category__id"] = category_id

    if user_id is not None:
        filter["id"] = id

    objects: list[Job] = Job.objects.filter(**filter).order_by("-updated_at").all()
    total_jobs_found = len(objects)
    if offset is not None and len(objects) > offset:
        objects = objects[offset:]
    jobs_found = []
    for count, job in enumerate(objects, start=1):
        jobs_found.append(
            JobResponse(
                company_username=job.company.username,
                category_name=job.category.name,
                **jsonable_encoder(job),
            )
        )
        if count == limit:
            break

    return JobsAvailable(total=total_jobs_found, jobs=jobs_found)


@router.get("/job/{id}", name="Get job by ID")
def get_job_by_id(
    id: int,
    whole: Annotated[
        bool, Query(description="Return all job details instead of just description")
    ] = True,
) -> JobDetails:
    """Get job details by ID"""
    try:
        target_job = Job.objects.get(id=id)
        if whole:
            return JobDetails(
                details=JobResponse(
                    company_username=target_job.company.username,
                    category_name=target_job.category.name,
                    **jsonable_encoder(target_job),
                ),
                description=target_job.description,
            )
        else:
            return JobDetails(description=target_job.description)
    except Job.DoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Job with id '{id}'  does not exist"
        )


@router.get("/categories", name="Category listings")
def get_categories_available(
    limit: Annotated[
        int, Query(description="Categories amount not to exceed", ge=1, le=100)
    ] = 50
) -> CategoriesAvailable:
    """Explore categories available"""
    categories = JobCategory.objects.order_by("-created_on").all()

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


@router.get("/category/{id}", name="Category Details")
def get_category_info(
    id: Annotated[int, Path(description="Category id")]
) -> CategoryInfo:
    """Specific category details"""
    try:
        category = JobCategory.objects.get(id=id)
        return CategoryInfo(
            jobs_amount=Job.objects.filter(category=category).count(),
            **jsonable_encoder(category),
        )
    except JobCategory.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job category with id '{id}' does not exist.",
        )


@router.post(
    "/job",
    name="Add new job",
)
@validate_category_id
def add_new_job(
    job_details: NewJob, user: Annotated[CustomUser, Depends(get_user)]
) -> UpdateJob:
    """Make new job entry"""
    job = Job.objects.create(
        company=user,
        category=JobCategory.objects.get(id=job_details.category_id),
        title=job_details.title,
        type=job_details.type,
        min_salary=job_details.min_salary,
        max_salary=job_details.max_salary,
        description=job_details.description,
        is_available=job_details.is_available,
    )
    job.save()
    return UpdateJob(**jsonable_encoder(job))


@router.patch("/job", name="Update existing job")
@validate_category_id
def update_existing_job(
    job_details: UpdateJob, user: Annotated[CustomUser, Depends(get_user)]
) -> UpdateJob:
    """Modify existing job"""
    get_value = lambda old, new: new if new is not None else old
    try:
        target_job = Job.objects.get(id=job_details.id, company=user)
        if job_details.category_id:
            target_job.category = JobCategory.objects.get(id=job_details.category_id)
        target_job.title = get_value(target_job.title, job_details.title)
        target_job.type = get_value(target_job.type, job_details.type)
        target_job.max_salary = get_value(target_job.max_salary, job_details.max_salary)
        target_job.min_salary = get_value(target_job.min_salary, job_details.min_salary)
        target_job.description = get_value(
            target_job.description, job_details.description
        )
        target_job.is_available = get_value(
            target_job.is_available, job_details.is_available
        )
        target_job.save()
        return UpdateJob(**jsonable_encoder(target_job))

    except Job.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only update a job that you created.",
        )


@router.delete("/job/{id}", name="Delete a job")
def delete_existing_job(
    id: Annotated[int, Path(description="Job id")],
    user: Annotated[CustomUser, Depends(get_user)],
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


@router.get("/job/appliers/{id}", name="Get users who applied a specific job")
def get_job_appliers(
    id: Annotated[int, Path(description="Job id")],
    user: Annotated[CustomUser, Depends(get_user)],
    offset: Annotated[int, Query(description="Offset value")] = 0,
    limit: Annotated[
        int, Query(description="Number of appliers not to exceed", ge=1, le=100)
    ] = 20,
) -> JobApplicants:
    """Get users who applied for a specific job"""
    try:
        target_job = Job.objects.get(id=id)
        if target_job.company.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view appliers for jobs you posted.",
            )
        appliers: list[CustomUser] = target_job.applicants.all()
        requested_appliers = appliers[offset : offset + limit]
        return JobApplicants(
            total=len(appliers),
            applicants=[jsonable_encoder(applier) for applier in requested_appliers],
        )
    except Job.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id '{id}' does not exist.",
        )


@router.get("/company/{id}", name="Get company details")
def get_company_details(id: Annotated[int, Path(description="Company id")]):
    """Get details about a specific company"""
    try:
        user = CustomUser.objects.get(id=id)
        return CompanyDetails(**jsonable_encoder(user))
    except CustomUser.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no company with id '{id}'",
        )


@router.get("/user/details", name="Get details about current user")
def get_user_details(
    user: Annotated[CustomUser, Depends(get_user)]
) -> CompleteApplicantDetails:
    """Get details about the current user"""
    return CompleteApplicantDetails(**jsonable_encoder(user))


@router.post("/user/apply/{id}", name="Apply for a specific job")
def apply_specific_job(
    id: Annotated[int, Path(description="Job id")],
    user: Annotated[CustomUser, Depends(get_user)],
) -> Feedback:
    """Apply for a job"""
    try:
        target_job = Job.objects.get(id=id)
        user.jobs_applied.add(target_job)
        user.save()
        return Feedback(detail="Job applied successfully")
    except Job.DoesNotExist:
        raise HTTPException(status_code=404, detail=f"There is no job with id '{id}'")


@router.delete("/user/apply/{id}", name="Unapply a speficic job")
def apply_specific_job(
    id: Annotated[int, Path(description="Job id")],
    user: Annotated[CustomUser, Depends(get_user)],
) -> Feedback:
    """Apply for a job"""
    try:
        target_job = Job.objects.get(id=id)
        user.jobs_applied.remove(target_job)
        user.save()
        return Feedback(detail="Job unapplied successfully")
    except Job.DoesNotExist:
        raise HTTPException(status_code=404, detail=f"There is no job with id '{id}'")


@router.get("/user/applied", name="Get jobs applied")
def get_jobs_applied(
    user: Annotated[CustomUser, Depends(get_user)],
    limit: Annotated[
        int, Query(description="Number of jobs not to exceed", ge=1, le=100)
    ] = 20,
) -> JobsAvailable:
    """Get jobs applied by the user"""
    jobs_applied: list[Job] = user.jobs_applied.order_by("-updated_at").all()
    total_jobs_applied = len(jobs_applied)
    jobs_found = []
    for count, job in enumerate(jobs_applied, start=1):
        jobs_found.append(
            JobResponse(
                company_username=job.company.username,
                category_name=job.category.name,
                **jsonable_encoder(job),
            )
        )
        if count == limit:
            break

    return JobsAvailable(total=total_jobs_applied, jobs=jobs_found)
