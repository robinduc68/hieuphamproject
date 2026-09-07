from peewee import CharField, BooleanField, TextField, ForeignKeyField
from .base import BaseModel
from .role import Role


class User(BaseModel):
    email         = CharField(max_length=255, unique=True)
    hashed_password= CharField(max_length=255)
    full_name     = CharField(max_length=255, null=True)
    phone         = CharField(max_length=30,  null=True)
    address       = TextField(null=True)
    is_active     = BooleanField(default=True)
    is_admin      = BooleanField(default=False)   # được vào trang quản trị
    # Quyền cụ thể trong trang quản trị lấy từ vai trò này (app/permissions.py)
    role          = ForeignKeyField(Role, backref="users", null=True, on_delete="SET NULL")

    class Meta:
        table_name = "users"
