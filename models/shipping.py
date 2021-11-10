from tortoise import fields
from models.base import BaseModel


class Shipping(BaseModel):
    id = fields.CharField(20, pk=True)
    due_datetime = fields.DatetimeField()
    site = fields.ForeignKeyField('models.Site')
    manufacturer_name = fields.CharField(20)
    manufacturer_address = fields.CharField(80)
    manufacturer_manager = fields.CharField(15)
    manufacturer_phone_number = fields.CharField(15)
    products = fields.JSONField()
    vehicle_number = fields.CharField(15)
    vehicle_type = fields.CharField(20)
    driver = fields.CharField(15)
    driver_phone_number = fields.CharField(15)
    shipping_status = fields.CharField(8, null=True, default='운송대기')
    receipt = fields.CharField(50, null=True)

    def __str__(self):
        return self.request

    class Meta:
        unique_together = (('due_datetime', 'site', 'manufacturer_address'))
        table = 'shipping'
