from peewee import CharField, TextField, BooleanField, IntegerField, DateField
from .base import BaseModel


class Post(BaseModel):
    """
    Bài viết của trang "Tin tức" (danh sách + trang chi tiết). Nội dung là HTML
    soạn bằng trình soạn thảo trong trang admin, ảnh chèn trong bài đã được
    upload sẵn nên chỉ lưu URL.
    """
    title        = CharField(max_length=255)
    slug         = CharField(max_length=255, unique=True)
    tag          = CharField(max_length=80, null=True)    # nhãn nhỏ trên card, VD "Kiến thức vải"
    subtitle     = TextField(null=True)                   # mô tả ngắn dưới tiêu đề ở trang chi tiết
    excerpt      = TextField(null=True)                   # tóm tắt hiện trên card danh sách
    content      = TextField(null=True)                   # HTML thân bài
    cover_image  = CharField(max_length=500, null=True)   # ảnh bìa (card + hero trang chi tiết)
    cover_color  = CharField(max_length=120, null=True)   # nền thay ảnh bìa khi chưa có ảnh
    published_at = DateField(null=True)                   # ngày hiện trên card
    is_published = BooleanField(default=True)
    sort_order   = IntegerField(default=0)

    class Meta:
        table_name = "posts"
