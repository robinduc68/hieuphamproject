from peewee import (
    CharField, TextField, DecimalField, BooleanField,
    IntegerField, ForeignKeyField, SmallIntegerField
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
    compare_at_price  = DecimalField(max_digits=14, decimal_places=0, null=True)  # giá gốc khi sale
    is_new            = BooleanField(default=False)
    is_active         = BooleanField(default=True)
    is_featured       = BooleanField(default=False)
    sort_order        = IntegerField(default=0)
    primary_color     = CharField(max_length=20, null=True)
    # 'apparel' = quần áo (trang chi tiết có size/tuỳ chỉnh may),
    # 'fabric'  = vải     (trang chi tiết bán theo mét, có thông số vải)
    product_type      = CharField(max_length=20, default="apparel")
    sku_code          = CharField(max_length=60, null=True)   # Mã sản phẩm
    specification     = TextField(null=True)                   # Quy cách
    fabric_width      = CharField(max_length=60, null=True)   # Khổ vải
    unit_label        = CharField(max_length=30, null=True)   # Đơn vị bán (mét, cái…)
    # Thuộc tính để lọc ở 2 trang kho lụa ngoài website
    pattern           = CharField(max_length=80, null=True)   # Họa tiết (VD: Thọ Dơi)
    color_tag         = CharField(max_length=40, null=True)   # Tone màu (VD: Hồng)
    silk_type         = CharField(max_length=100, null=True)  # Loại lụa (trang 100% tơ tằm)

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
    size          = CharField(max_length=20)
    stock         = IntegerField(default=0)
    is_available  = BooleanField(default=True)
    sort_order    = SmallIntegerField(default=0)

    class Meta:
        table_name = "product_sizes"
        indexes    = ((("product", "size"), True),)  # unique together
