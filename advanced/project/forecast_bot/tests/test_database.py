import pytest
import pytest_asyncio
import tempfile
import os

from db.database import Database  # убедись, что путь верный


# =========================
# Async Fixture
# =========================
@pytest_asyncio.fixture
async def db():
    """
    Создаёт временную базу данных для каждого теста.
    """
    db_path = tempfile.mktemp(suffix=".db")
    database = Database(db_path)
    await database.connect()
    yield database
    await database.close()
    os.remove(db_path)


# =========================
# Тести
# =========================

@pytest.mark.asyncio
async def test_add_and_get_user(db: Database):
    await db.add_user(telegram_id=1, full_name="John Doe", username="john")
    user = await db.get_user(telegram_id=1)
    assert user is not None
    assert user["telegram_id"] == 1
    assert user["full_name"] == "John Doe"
    assert user["username"] == "john"


@pytest.mark.asyncio
async def test_add_user_ignore_duplicate(db: Database):
    await db.add_user(1, "John Doe", "john")
    await db.add_user(1, "John Changed", "changed")
    user = await db.get_user(1)
    assert user["full_name"] == "John Doe"
    assert user["username"] == "john"


@pytest.mark.asyncio
async def test_save_and_get_location(db: Database):
    await db.save_location(
        telegram_id=1,
        label="home",
        lat=50.45,
        lon=30.52,
        name="Kyiv"
    )
    loc = await db.get_location_by_label(1, "home")
    assert loc is not None
    assert loc["label"] == "home"
    assert loc["lat"] == 50.45
    assert loc["lon"] == 30.52
    assert loc["name"] == "Kyiv"


@pytest.mark.asyncio
async def test_update_location_same_label(db: Database):
    await db.save_location(1, "home", 10.0, 10.0, "Old City")
    await db.save_location(1, "home", 20.0, 20.0, "New City")
    loc = await db.get_location_by_label(1, "home")
    assert loc["lat"] == 20.0
    assert loc["lon"] == 20.0
    assert loc["name"] == "New City"


@pytest.mark.asyncio
async def test_get_locations(db: Database):
    await db.save_location(1, "home", 1.0, 1.0)
    await db.save_location(1, "work", 2.0, 2.0)
    locations = await db.get_locations(1)
    assert len(locations) == 2
    labels = {loc["label"] for loc in locations}
    assert labels == {"home", "work"}


@pytest.mark.asyncio
async def test_delete_location(db: Database):
    await db.save_location(1, "home", 1.0, 1.0)
    await db.delete_location(1, "home")
    loc = await db.get_location_by_label(1, "home")
    assert loc is None
