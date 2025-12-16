import aiosqlite
from typing import Optional, List, Tuple
import datetime

class Database:
    def __init__(self, path: str):
        self.path = path
        self._conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        self._conn = await aiosqlite.connect(self.path)
        # чтобы получать словари, можно использовать row_factory
        self._conn.row_factory = aiosqlite.Row
        await self._create_tables()

    async def close(self):
        if self._conn:
            await self._conn.close()

    async def _create_tables(self):
        assert self._conn is not None
        await self._conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            full_name TEXT,
            username TEXT,
            created_at TEXT
        );
        """)
        await self._conn.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            label TEXT,          -- 'home', 'work' или custom
            lat REAL,
            lon REAL,
            name TEXT,           -- имя места/город (по желанию)
            created_at TEXT,
            UNIQUE(telegram_id, label)   -- одно значение label на пользователя
        );
        """)
        await self._conn.commit()

    # ---- users ----
    async def add_user(self, telegram_id: int, full_name: str, username: Optional[str]):
        assert self._conn is not None
        now = datetime.datetime.utcnow().isoformat()
        await self._conn.execute("""
        INSERT OR IGNORE INTO users (telegram_id, full_name, username, created_at)
        VALUES (?, ?, ?, ?)
        """, (telegram_id, full_name, username, now))
        await self._conn.commit()

    async def get_user(self, telegram_id: int) -> Optional[aiosqlite.Row]:
        assert self._conn is not None
        cursor = await self._conn.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row

    # ---- locations ----
    async def save_location(self, telegram_id: int, label: str, lat: float, lon: float, name: Optional[str] = None):
        """
        Сохраняет локацию. Если уже есть запись с same (telegram_id, label) — заменяет.
        """
        assert self._conn is not None
        now = datetime.datetime.utcnow().isoformat()
        await self._conn.execute("""
        INSERT INTO locations (telegram_id, label, lat, lon, name, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(telegram_id, label) DO UPDATE SET lat=excluded.lat, lon=excluded.lon, name=excluded.name, created_at=excluded.created_at;
        """, (telegram_id, label, lat, lon, name, now))
        await self._conn.commit()

    async def get_locations(self, telegram_id: int) -> List[aiosqlite.Row]:
        assert self._conn is not None
        cursor = await self._conn.execute("SELECT * FROM locations WHERE telegram_id = ?", (telegram_id,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

    async def get_location_by_label(self, telegram_id: int, label: str) -> Optional[aiosqlite.Row]:
        assert self._conn is not None
        cursor = await self._conn.execute("SELECT * FROM locations WHERE telegram_id = ? AND label = ?", (telegram_id, label))
        row = await cursor.fetchone()
        await cursor.close()
        return row

    async def delete_location(self, telegram_id: int, label: str):
        assert self._conn is not None
        await self._conn.execute("DELETE FROM locations WHERE telegram_id = ? AND label = ?", (telegram_id, label))
        await self._conn.commit()
