from models.manufacturer import Manufacturer
from sanic.exceptions import abort


class ManufacturerService:

    @staticmethod
    async def create_manufacturer(manufacturer_name: str, manufacturer_address: str, manufacturer_phone_number: str, manufacturer_manager: str):
        manufacturer = await Manufacturer.create(name=manufacturer_name, address=manufacturer_address, phone_number=manufacturer_phone_number, manager=manufacturer_manager)
        return manufacturer

    @staticmethod
    async def select_manufacturers():
        manufacturers = await Manufacturer.all()
        return manufacturers

    @staticmethod
    async def select_manufacturer(id: int):
        manufacturer = await Manufacturer.get_or_none(id=id)
        if not manufacturer:
            raise abort(404)
        return manufacturer

    @staticmethod
    async def patch_manufacturer(id: int, manufacturer_name: str, manufacturer_address: str, manufacturer_phone_number: str, manufacturer_manager: str):
        await Manufacturer.select_for_update().get(id=id).update(name=manufacturer_name, address=manufacturer_address, manager=manufacturer_manager, phone_number=manufacturer_phone_number)
        manufacturer = await Manufacturer.get(id=id)
        return manufacturer
