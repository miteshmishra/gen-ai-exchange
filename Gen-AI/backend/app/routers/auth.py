from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, datetime
from typing import Any, Dict, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from ..core.security import create_access_token, get_current_user
from ..core.config import settings
from ..db.session import get_db
from ..models.database import User as DBUser

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_user_by_email(email: str, db: Session) -> DBUser:
    return db.query(DBUser).filter(DBUser.email == email).first()

async def authenticate_user(email: str, password: str, db: Session) -> DBUser:
    user = await get_user_by_email(email, db)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user



@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "id": 1
                    }
                }
            }
        },
        400: {
            "description": "Email already registered or registration failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already registered"}
                }
            }
        }
    }
)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user in the system.
    
    Parameters:
    - **email**: Valid email address
    - **password**: Strong password (min 8 characters)
    - **full_name**: User's full name
    """
    # Check if user exists
    if await get_user_by_email(user_data.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        # Create new user
        db_user = DBUser(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "email": db_user.email,
            "full_name": db_user.full_name,
            "id": db_user.id
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )

@router.post(
    "/login",
    response_model=dict,
    responses={
        200: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "full_name": "John Doe"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
                }
            }
        }
    }
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Authenticate user and return JWT token.
    
    The endpoint expects form data with:
    - **username**: User's email address
    - **password**: User's password
    
    Returns a JWT token that should be used in subsequent requests in the Authorization header.
    """
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }

@router.get(
    "/me",
    response_model=dict,
    responses={
        200: {
            "description": "Current user information",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "John Doe"
                    }
                }
            }
        },
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        }
    }
)
async def get_user_me(
    current_user: DBUser = Depends(get_current_user)
) -> Any:
    """
    Get current authenticated user's information.
    
    Requires a valid JWT token in the Authorization header.
    Returns the user's profile information.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }
