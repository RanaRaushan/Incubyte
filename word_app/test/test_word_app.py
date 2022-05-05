import pytest
from httpx import AsyncClient

import main
from db.database import get_async_session as get_db, Base
from word_app.test.conftest import override_get_db, engine
from word_app.test.test_utils import TestUtils

main.app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_create_new_word():
    data = TestUtils.get_new_word_create_response()
    async with AsyncClient(app=main.app, base_url="http://test",
                           headers={"Content-Type": "application/x-www-form-urlencoded"}) as client:
        response = await client.post("/create", data=data)
    assert response.status_code == 302
    assert response.next_request.url == "http://test/word"


@pytest.mark.asyncio
async def test_create_new_word_redirect():
    data = TestUtils.get_new_word_create_response()
    async with AsyncClient(app=main.app, base_url="http://test",
                           headers={"Content-Type": "application/x-www-form-urlencoded"}) as client:
        response = await client.post("/create", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.url == "http://test/word"


@pytest.mark.asyncio
async def test_get_update_existing_word():
    async with AsyncClient(app=main.app, base_url="http://test",
                           headers={"Content-Type": "application/x-www-form-urlencoded"}) as client:
        response = await client.get("/word/update?id=1", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_update_existing_word():
    data = TestUtils.get_new_updated_response(word_id="1")
    async with AsyncClient(app=main.app, base_url="http://test",
                           headers={"Content-Type": "application/x-www-form-urlencoded"}) as client:
        response = await client.post("/word/update?id=1", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.url == "http://test/word"


@pytest.mark.asyncio
async def test_get_all_word():
    async with AsyncClient(app=main.app, base_url="http://test",) as client:
        response = await client.get("/word")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_existing_word():
    data = TestUtils.get_new_updated_response(word_id="1")
    async with AsyncClient(app=main.app, base_url="http://test",
                           headers={"Content-Type": "application/x-www-form-urlencoded"}) as client:
        response = await client.post("/word/delete/1", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.url == "http://test/word"


@pytest.mark.asyncio
async def test_delete_non_existing_word():
    data = TestUtils.get_new_updated_response(word_id="1")
    async with AsyncClient(app=main.app, base_url="http://test",
                           headers={"Content-Type": "application/x-www-form-urlencoded"}) as client:
        response = await client.post("/word/delete/1", data=data, follow_redirects=True)
    assert response.status_code == 401
    assert response.json()['error_type'] == "WORD_NOT_FOUND"


@pytest.mark.asyncio
async def test_drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
