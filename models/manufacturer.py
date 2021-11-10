from tortoise import fields
from models.base import BaseModel, EntityMixin


class Manufacturer(BaseModel, EntityMixin):
    manager = fields.CharField(15)
    name = fields.CharField(15)

    class Meta:
        unique_together = (('manager', 'phone_number'), ('name', 'address'))
        table = 'manufacturer'

    def __str__(self):
        return f'제조사 : {self.name} 담당자 : {self.manager}'
