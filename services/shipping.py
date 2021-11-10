import random
import string
from datetime import datetime
from models.shipping import Shipping
from models.site import Site
import json
from typing import List, Dict
from sanic.exceptions import abort


class ShippingService:

    @ staticmethod
    async def create_shipping(due_datetime: datetime, site_address: str, site_phone_number: str, manufacturer_name: str, manufacturer_manager: str, manufacturer_phone_number: str, products: List[Dict],
                              manufacturer_address: str, vehicle_number: str, vehicle_type: str, driver: str, driver_phone_number: str):

        async def generate_shipping_id(N=4):
            while True:
                random_key = ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=4))
                shipping_id = f'{due_datetime.year}{due_datetime.month}{due_datetime.day}{due_datetime.hour}{due_datetime.minute}DT{random_key}'
                existence = await Shipping.exists(id=shipping_id)
                if not existence:
                    break

            return shipping_id

        shipping_id = await generate_shipping_id(4)
        site, _ = await Site.get_or_create(address=site_address,
                                           phone_number=site_phone_number)

        await Shipping.create(id=shipping_id, site=site, manufacturer_address=manufacturer_address, manufacturer_name=manufacturer_name,
                              manufacturer_manager=manufacturer_manager, manufacturer_phone_number=manufacturer_phone_number, products=json.dumps(products, ensure_ascii=False), due_datetime=due_datetime,
                              vehicle_number=vehicle_number, vehicle_type=vehicle_type, driver=driver, driver_phone_number=driver_phone_number)

    @ staticmethod
    async def select_shippings():
        shippings = await Shipping.all().order_by('id').prefetch_related('site')
        return shippings

    @ staticmethod
    async def select_shipping(id: str):
        shipping = await Shipping.get_or_none(id=id).prefetch_related('site')
        if not shipping:
            raise abort(404)
        return shipping

    @ staticmethod
    async def patch_shipping(id, due_datetime: datetime, site_address: str, site_phone_number: str, manufacturer_name: str, manufacturer_manager: str, manufacturer_phone_number: str, products: List[Dict],
                             manufacturer_address: str, vehicle_number: str, vehicle_type: str, driver: str, driver_phone_number: str):
        site, _ = await Site.get_or_create(address=site_address, phone_number=site_phone_number)
        await Shipping.select_for_update().get_or_none(id=id).prefetch_related('site').update(due_datetime=due_datetime, site=site, manufacturer_name=manufacturer_name,
                                                                                              manufacturer_address=manufacturer_address, manufacturer_manager=manufacturer_manager,
                                                                                              manufacturer_phone_number=manufacturer_phone_number, products=json.dumps(products, ensure_ascii=False), vehicle_number=vehicle_number, vehicle_type=vehicle_type,
                                                                                              driver=driver, driver_phone_number=driver_phone_number)
        shipping = await Shipping.get(id=id).prefetch_related('site')
        return shipping

    @ staticmethod
    async def patch_status(id: str, shipping_status: str, receipt: str = None):
        if shipping_status == '운송완료':
            assert receipt is not None
            await Shipping.select_for_update().get_or_none(id=id).prefetch_related('site').update(
                shipping_status=shipping_status, receipt=receipt)
        else:
            await Shipping.select_for_update().get_or_none(id=id).prefetch_related('site').update(shipping_status=shipping_status)
        shipping = await Shipping.get(id=id).prefetch_related('site')
        return shipping
