from tortoise import fields
from models.base import BaseModel


class Product(BaseModel):
    manufacturer = fields.ForeignKeyField(
        'models.Manufacturer', on_delete=fields.CASCADE)
    name = fields.CharField(50)
    standard = fields.CharField(15, null=True)
    approval = fields.CharField(50)

    def __str__(self):
        return f'{self.name} {self.standard} {self.manufacturer.name}'

    class Meta:
        unique_together = (('manufacturer', 'name', 'standard'))
        table = 'product'
