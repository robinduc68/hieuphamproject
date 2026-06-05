from peewee import (
    CharField, TextField, DecimalField, BooleanField,
    IntegerField, ForeignKeyField
)
from .base import BaseModel
from .category import Category, SubCategory
from .collection import Collection


class Product(BaseModel):
    name              = CharField(max_length=255)
    slug              = CharField(max_length=255, unique=True)
    price             = DecimalField(max_digits=14, decimal_places=0)
    description       = TextField(null=True)
    fabric            = TextField(null=True)
    care_instructions = TextField(null=True)
    shipping_info     = TextField(null=True)
    category          = ForeignKeyField(Category,    backref="products", null=True, on_delete="SET NULL")
    subcategory       = ForeignKeyField(SubCategory, backref="products", null=True, on_delete="SET NULL")
    collection        = ForeignKeyField(Collection,  backref="products", null=True, on_delete="SET NULL")
    is_new            = BooleanField(default=False)
    is_active         = BooleanField(default=True)
    is_featured       = BooleanField(default=False)
    sort_order        = IntegerField(default=0)
    primary_color     = CharField(max_length=20, null=True)  # HEX cho placeholder UI

    class Meta:
        table_name = "products"


class ProductImage(BaseModel):
    product    = ForeignKeyField(Product, backref="images", on_delete="CASCADE")
    url        = CharField(max_length=500)
    alt_text   = CharField(max_length=255, null=True)
    sort_order = IntegerField(default=0)
    is_primary = BooleanField(default=False)

    class Meta:
        table_name  = "product_images"
        indexes     = ((("product", "sort_order"), False),)


class ProductSize(BaseModel):
    product       = ForeignKeyField(Product, backref="sizes", on_delete="CASCADE")
    size          = CharField(max_length=20)    # 32, 34, S, M, L …
    stock         = IntegerField(default=0)
    is_available  = BooleanField(default=True)

    class Meta:
        table_name = "product_sizes"
        indexes    = ((("product", "size"), True),)  # unique together
