from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.model.user import User
from app.schemas.user_schema import UserCreate, UserLogin,AdminUserCreate
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.email == user.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered..")

        new_user = User(
            email=user.email,
            hashed_password=hash_password(user.password),
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {"message": "User registered successfully"}
    except SQLAlchemyError as db_err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        ) from db_err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post("/admin/register")
async def admin_register(user: AdminUserCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.email == user.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            email=user.email,
            hashed_password=hash_password(user.password),
            role = user.role
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {"message": "User registered successfully"}
    except SQLAlchemyError as db_err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register admin user"
        ) from db_err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: AsyncSession = Depends(get_db)):
    try:
        email = form_data.username 
        password = form_data.password

        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": str(user.id),"role": user.role})
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except SQLAlchemyError as db_err:
        logger.exception("Database error during login")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        ) from db_err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.get("/users")
async def users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User))
        return result.scalars().all()
    except SQLAlchemyError as db_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        ) from db_err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))