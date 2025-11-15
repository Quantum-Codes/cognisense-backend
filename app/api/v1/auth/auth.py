from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from app.core.config import settings
from app.core.supabase_client import supabase

router = APIRouter()
bearer_scheme = HTTPBearer()


# Pydantic model for signup and login requests
class SignupLoginRequest(BaseModel):
    email: EmailStr
    password: str


async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """Verify token with Supabase and return the user payload using supabase-py library."""
    token = credentials.credentials

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SUPABASE_URL or SUPABASE_KEY not configured")

    try:
        user = supabase.auth.get_user(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or expired token: {str(e)}")

    if not user or not getattr(user, "user", None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return user.user


@router.get("/me")
async def read_current_user(current_user=Depends(get_current_user)):
    """Return the authenticated Supabase user payload."""
    return {"user": current_user}


@router.post("/signup")
async def signup(data: SignupLoginRequest):
    """Register a new user with Supabase (email & password)."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SUPABASE_URL or SUPABASE_KEY not configured")

    try:
        result = supabase.auth.sign_up({"email": data.email, "password": data.password})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Signup failed: {str(e)}")

    if not result or not getattr(result, "user", None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signup failed: No user returned")

    return {"user": result.user, "session": result.session}

@router.post("/login")
async def login(data: SignupLoginRequest):
    """Authenticate a user with Supabase (email & password)."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SUPABASE_URL or SUPABASE_KEY not configured")

    try:
        result = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login failed: {str(e)}")

    if not result or not getattr(result, "user", None) or not getattr(result, "session", None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed: Invalid credentials or no session returned")

    return {"user": result.user, "session": result.session}