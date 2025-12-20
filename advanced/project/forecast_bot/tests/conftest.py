import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest_asyncio
from db.database import Database


@pytest_asyncio.fixture
async def db(tmp_path):
    db_path = tmp_path / "test.db"

    database = Database(str(db_path))
    await database.connect()

    yield database

    await database.close()
