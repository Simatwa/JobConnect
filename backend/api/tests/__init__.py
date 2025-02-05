from os import getenv
from api import app
from fastapi.testclient import TestClient

if getenv("FAKE_DATA", "") == "true":
    from api.fake_data import FakeJob, FakeUsers

    FakeUsers().users(3)
    fake_job = FakeJob()
    fake_job.category(4)
    fake_job.job(5)

client = TestClient(app, base_url="http://testserver/api")
