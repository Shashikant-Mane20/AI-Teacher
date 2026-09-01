from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import create_access_token, current_user, hash_password, verify_password
from app.database import find_profile, find_user, insert_user, save_profile
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from app.schemas.profile import StudentProfileResponse, StudentProfileUpdate

router = APIRouter(prefix="/api/v1", tags=["authentication and profiles"])


@router.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    email = str(payload.email).lower()
    if await find_user(email):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = {"user_id": uuid4().hex, "name": payload.name, "email": email, "password_hash": hash_password(payload.password)}
    await insert_user(user)
    return {"access_token": create_access_token(user["user_id"]), "user_id": user["user_id"], "name": user["name"]}


@router.post("/auth/login", response_model=AuthResponse)
async def login(payload: LoginRequest):
    user = await find_user(str(payload.email).lower())
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": create_access_token(user["user_id"]), "user_id": user["user_id"], "name": user["name"]}


@router.get("/auth/me", response_model=UserResponse)
async def me(user: dict = Depends(current_user)):
    return {"user_id": user["user_id"], "name": user["name"], "email": user["email"]}


@router.get("/students/me/profile", response_model=StudentProfileResponse)
async def get_my_profile(user: dict = Depends(current_user)):
    profile = await find_profile(user["user_id"])
    if profile is None:
        profile = {"user_id": user["user_id"], "email": user["email"], "name": user["name"], "avatar_url": None}
    return profile


@router.put("/students/me/profile", response_model=StudentProfileResponse)
async def update_my_profile(payload: StudentProfileUpdate, user: dict = Depends(current_user)):
    profile = payload.model_dump()
    profile.update({"user_id": user["user_id"], "email": user["email"], "name": payload.name or user["name"]})
    await save_profile(profile)
    return profile
