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


class Manufacturer(BaseModel, EntityMixin):
    manager = fields.CharField(15)
    name = fields.CharField(15)

    class Meta:
        unique_together = (('manager', 'phone_number'), ('name', 'address'))
        table = 'manufacturer'

    def __str__(self):
        return f'제조사 : {self.name} 담당자 : {self.manager}'


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


class Site(BaseModel, EntityMixin):

    class Meta:
        unique_together = (('address', 'phone_number'),)
        table = 'site'

    def __str__(self):
        return f'현장주소 : {self.address} 연락처 : {self.phone_number}'


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
