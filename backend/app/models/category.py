from peewee import CharField, TextField, BooleanField, IntegerField, ForeignKeyField
from .base import BaseModel


class Category(BaseModel):
    """Danh mục cấp 1: Modern Heritage, WomenSwear, MenSwear"""
    name        = CharField(max_length=120)
    slug        = CharField(max_length=120, unique=True)
    description = TextField(null=True)
    image_url   = CharField(max_length=500, null=True)
    is_active   = BooleanField(default=True)
    sort_order  = IntegerField(default=0)

    class Meta:
        table_name = "categories"


class SubCategory(BaseModel):
    """Danh mục cấp 2: Áo Dài Madame, FirstLady, Bà Ba Mademoiselle …"""
    category    = ForeignKeyField(Category, backref="subcategories", on_delete="CASCADE")
    name        = CharField(max_length=120)
    slug        = CharField(max_length=120, unique=True)
    description = TextField(null=True)
    image_url   = CharField(max_length=500, null=True)
    is_active   = BooleanField(default=True)
    sort_order  = IntegerField(default=0)

    class Meta:
        table_name = "subcategories"
