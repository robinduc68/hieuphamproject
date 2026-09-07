from peewee import CharField, TextField, BooleanField
from .base import BaseModel


class Role(BaseModel):
    """
    Vai trò của tài khoản admin. `permissions` là JSON danh sách mã quyền
    (xem app/permissions.py); vai trò toàn quyền lưu ["*"].
    """
    name        = CharField(max_length=100, unique=True)
    description = CharField(max_length=255, null=True)
    permissions = TextField(null=True)
    is_system   = BooleanField(default=False)   # vai trò gốc, không cho xoá

    class Meta:
        table_name = "roles"
