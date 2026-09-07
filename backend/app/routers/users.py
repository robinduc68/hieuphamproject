from fastapi import APIRouter, HTTPException, Depends, status
from peewee import DoesNotExist, IntegrityError

from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserUpdate, UserOut, TokenOut, user_out
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: UserRegister, _db=Depends(get_db)):
    try:
        user = User.create(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            phone=data.phone,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email đã được sử dụng.",
        )
    token = create_access_token(user.id)
    return TokenOut(
        access_token=token,
        user=user_out(user),
    )


@router.post("/login", response_model=TokenOut)
def login(data: UserLogin, _db=Depends(get_db)):
    try:
        user = User.get(User.email == data.email)
    except DoesNotExist:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng.")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị khoá.")

    token = create_access_token(user.id)
    return TokenOut(
        access_token=token,
        user=user_out(user),
    )


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return user_out(current_user)


@router.put("/me", response_model=UserOut)
def update_me(data: UserUpdate, current_user: User = Depends(get_current_user)):
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(current_user, field, val)
    current_user.save()
    return user_out(current_user)


@router.put("/me/password", status_code=204)
def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
):
    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu cũ không đúng.")
    current_user.hashed_password = hash_password(new_password)
    current_user.save()
