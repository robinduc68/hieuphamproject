from peewee import CharField, DecimalField, BooleanField, SmallIntegerField
from .base import BaseModel


class CustomizationOption(BaseModel):
    group_key        = CharField(max_length=60)
    group_label      = CharField(max_length=120)
    option_key       = CharField(max_length=60)
    option_label     = CharField(max_length=120)
    price_adjustment = DecimalField(max_digits=14, decimal_places=0, default=0)
    sort_order       = SmallIntegerField(default=0)
    is_active        = BooleanField(default=True)

    class Meta:
        table_name = "customization_options"
        indexes    = ((("group_key", "option_key"), True),)
