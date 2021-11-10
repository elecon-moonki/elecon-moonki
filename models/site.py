from models.base import BaseModel, EntityMixin


class Site(BaseModel, EntityMixin):

    class Meta:
        unique_together = (('address', 'phone_number'),)
        table = 'site'

    def __str__(self):
        return f'현장주소 : {self.address} 연락처 : {self.phone_number}'
