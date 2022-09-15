from fastapi.testclient import TestClient

from engine.routes.base import app
from engine.routes.models import ImportBatch, ImportChunk, Type
import datetime


def test_can_import_batch():
    client = TestClient(app)
    batch = ImportBatch(items=[ImportChunk(id='string', type=0)], updateDate=datetime.datetime.utcnow())
    response = client.post("/imports", batch.json())
    assert response.status_code == 422, "Test post passed"