from .base import BaseModel
from .category import Category, SubCategory
from .collection import Collection
from .product import Product, ProductImage, ProductSize
from .role import Role
from .user import User
from .order import Order, OrderItem
from .newsletter import NewsletterSubscription
from .customization import CustomizationOption
from .setting import SiteSetting
from .post import Post

ALL_MODELS = [
    Category, SubCategory,
    Collection,
    Product, ProductImage, ProductSize,
    Role, User,
    Order, OrderItem,
    NewsletterSubscription,
    CustomizationOption,
    SiteSetting,
    Post,
]
