from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
database = client[settings.mongo_db]
users_collection = database.users
profiles_collection = database.student_profiles

_memory_users: dict[str, dict] = {}
_memory_profiles: dict[str, dict] = {}


async def mongo_available() -> bool:
    try:
        await client.admin.command("ping")
        return True
    except Exception:
        return False


def using_memory_fallback() -> bool:
    return settings.environment == "development" and settings.mongo_uri.startswith("mongodb://localhost")


async def find_user(email: str) -> dict | None:
    cached = _memory_users.get(email.lower())
    if cached:
        return cached
    if using_memory_fallback() or not await mongo_available():
        return None
    return await users_collection.find_one({"email": email.lower()})


async def find_user_by_id(user_id: str) -> dict | None:
    cached = next((user for user in _memory_users.values() if user["user_id"] == user_id), None)
    if cached:
        return cached
    if using_memory_fallback() or not await mongo_available():
        return None
    return await users_collection.find_one({"user_id": user_id}, {"_id": 0})


async def insert_user(user: dict) -> None:
    _memory_users[user["email"]] = user
    if using_memory_fallback() or not await mongo_available():
        return
    await users_collection.insert_one(user)


async def save_profile(profile: dict) -> None:
    _memory_profiles[profile["user_id"]] = profile
    if using_memory_fallback() or not await mongo_available():
        return
    await profiles_collection.replace_one({"user_id": profile["user_id"]}, profile, upsert=True)


async def find_profile(user_id: str) -> dict | None:
    cached = _memory_profiles.get(user_id)
    if cached:
        return cached
    if using_memory_fallback() or not await mongo_available():
        return None
    return await profiles_collection.find_one({"user_id": user_id}, {"_id": 0})
