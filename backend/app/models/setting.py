from peewee import CharField, TextField
from .base import BaseModel


class SiteSetting(BaseModel):
    """
    Cấu hình nội dung website do admin sửa được (video hero, bảng hướng dẫn
    chọn size, bảng định mức may đo…). `value` lưu JSON dạng chuỗi để mỗi
    cấu hình tự do về cấu trúc mà không cần thêm bảng mới.
    """
    key   = CharField(max_length=80, unique=True)
    value = TextField(null=True)

    class Meta:
        table_name = "site_settings"
