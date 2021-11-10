from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class EntityMixin():
    address = fields.CharField(80)
    phone_number = fields.CharField(15)
