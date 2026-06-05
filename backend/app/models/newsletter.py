from peewee import CharField, BooleanField
from .base import BaseModel


class NewsletterSubscription(BaseModel):
    email      = CharField(max_length=255, unique=True)
    full_name  = CharField(max_length=255, null=True)
    is_active  = BooleanField(default=True)

    class Meta:
        table_name = "newsletter_subscriptions"
