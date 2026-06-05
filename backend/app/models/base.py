import datetime
from peewee import Model, DateTimeField, AutoField
from app.database import database


class BaseModel(Model):
    id         = AutoField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    class Meta:
        database = database
