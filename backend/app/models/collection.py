from peewee import CharField, TextField, BooleanField, IntegerField
from .base import BaseModel


class Collection(BaseModel):
    """Bộ sưu tập: Timeless Perfection, A Wedding Dress …"""
    name        = CharField(max_length=180)
    slug        = CharField(max_length=180, unique=True)
    subtitle    = CharField(max_length=255, null=True)
    description = TextField(null=True)
    cover_url   = CharField(max_length=500, null=True)
    gradient    = CharField(max_length=255, null=True)   # CSS gradient string
    accent_color= CharField(max_length=20, null=True)    # HEX
    is_active   = BooleanField(default=True)
    sort_order  = IntegerField(default=0)

    class Meta:
        table_name = "collections"
