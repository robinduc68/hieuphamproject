from peewee import CharField, BooleanField, TextField
from .base import BaseModel


class User(BaseModel):
    email         = CharField(max_length=255, unique=True)
    hashed_password= CharField(max_length=255)
    full_name     = CharField(max_length=255, null=True)
    phone         = CharField(max_length=30,  null=True)
    address       = TextField(null=True)
    is_active     = BooleanField(default=True)
    is_admin      = BooleanField(default=False)

    class Meta:
        table_name = "users"
