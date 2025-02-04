import pytest
from . import client
from api import v1_router
from api.v1.models import NewJob, UpdateJob

request_headers = {"Content-Type": "application/json", "Authorization": "Bearer None"}

credentials_payload = {
    "username": "developer",
    "password": "development",
    "grant_type": "password",
}


def auth_request_headers() -> dict:
    resp = client.post(v1_router.url_path_for("User token"), data=credentials_payload)
    feedback = resp.json()
    assert resp.is_success
    request_headers["Authorization"] = "Bearer " + feedback["access_token"]
    return request_headers


def test_job_listings():
    resp = client.get(v1_router.url_path_for("Job listings"))
    assert resp.is_success


def test_get_job_by_id():
    resp = client.get(v1_router.url_path_for("Get job by ID", id=1))
    assert resp.is_success


def get_categories_available():
    resp = client.get(v1_router.url_path_for("Category listings"))
    assert resp.is_success


def test_get_category_details():
    resp = client.get(v1_router.url_path_for("Category Details", id=1))
    assert resp.is_success


def test_generate_new_token():
    resp = client.patch(
        v1_router.url_path_for("Generate new token"), headers=auth_request_headers()
    )
    assert resp.is_success


def test_add_new_job():
    resp = client.post(
        v1_router.url_path_for("Add new job"),
        json=NewJob.model_config["json_schema_extra"]["example"],
        headers=auth_request_headers(),
    )
    assert resp.is_success


def test_update_existing_job():
    resp = client.post(
        v1_router.url_path_for("Add new job"),
        json=NewJob.model_config["json_schema_extra"]["example"],
        headers=auth_request_headers(),
    )
    assert resp.is_success
    resp1 = client.patch(
        v1_router.url_path_for("Update existing job"),
        json=resp.json(),
        headers=auth_request_headers(),
    )
    assert resp1.is_success


def test_delete_a_job():
    resp = client.post(
        v1_router.url_path_for("Add new job"),
        json=NewJob.model_config["json_schema_extra"]["example"],
        headers=auth_request_headers(),
    )
    assert resp.is_success
    job_added = UpdateJob(**resp.json())
    resp1 = client.delete(
        v1_router.url_path_for("Delete a job", id=job_added.id),
        headers=auth_request_headers(),
    )
    assert resp1.is_success


def test_get_company_details():
    resp = client.get(v1_router.url_path_for("Get company details", id=1))
    assert resp.is_success


def test_get_current_user_details():
    resp = client.get(
        v1_router.url_path_for(
            "Get details about current user",
        ),
        headers=auth_request_headers(),
    )
    assert resp.is_success


def test_apply_specific_job():
    resp = client.post(
        v1_router.url_path_for("Apply for a specific job", id=1),
        headers=auth_request_headers(),
    )
    assert resp.is_success


def test_unapply_specific_job():
    resp = client.post(
        v1_router.url_path_for("Apply for a specific job", id=2),
        headers=auth_request_headers(),
    )
    assert resp.is_success
    resp1 = client.delete(
        v1_router.url_path_for("Unapply a speficic job", id=2),
        headers=auth_request_headers(),
    )
    assert resp1.is_success


def test_get_jobs_applied():
    resp = client.get(
        v1_router.url_path_for("Get jobs applied"),
        headers=auth_request_headers(),
    )
    assert resp.is_success
