import asyncio
from sqlalchemy.dialects.postgresql import insert
from app.database_settings import DB_MANAGER
from app.models import APIKeyUsage


async def seed_tru_api_key():
    """Seed 'Tru' API key """
    DB_MANAGER.initialize()
    async with DB_MANAGER.session() as session:
        try:
            stmt = insert(APIKeyUsage).values(
                company_name="Tru",
                api_key="tru",
                usage_count=0,
                last_request_at=None,
            ).on_conflict_do_nothing(index_elements=["api_key"])

            await session.execute(stmt)
            await session.commit()

            print("[seed_tru_api_key] Tru API key seeded (or already exists).")
        except Exception as e:
            await session.rollback()
            print(f"[seed_tru_api_key]  Seeding failed: {e}")


if __name__ == "__main__":
    asyncio.run(seed_tru_api_key())
