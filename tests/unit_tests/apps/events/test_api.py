import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from de_demo.apps.events.api.routes import get_buffer, router


class Buffer:
    def __init__(self):
        self.buff = []

    async def append(self, item):
        self.buff.append(item)


@pytest.fixture(scope='function')
def test_buff():
    return Buffer()


@pytest.fixture(scope='function')
def events_api_client(test_buff):
    async def get_test_buffer():
        return test_buff

    app = FastAPI(title="de-demo-test")
    app.include_router(router)
    app.dependency_overrides[get_buffer] = get_test_buffer

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides = {}


@pytest.mark.parametrize(
    'data, status_code',
    [
        ({"unknown": "field"}, 422),
        ({"dt": "2000-10-11T12:13:14",
          "name": "view",
          "user_id": 1,
          "url": "http://test/page1",
          "obj": "page",
          "obj_id": "page1",
          "exp": {"exp1": "A"}
          }, 200),
    ]
)
def test_event_validation(events_api_client, test_buff, data, status_code):
    response = events_api_client.post(
        "/events",
        json=data,
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        assert len(test_buff.buff) == 1
