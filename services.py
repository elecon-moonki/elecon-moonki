from typing import List, Dict
from models import Site, Manufacturer, Shipping, Product
from datetime import datetime
import json
from sanic.exceptions import abort
import random
import string
from tortoise.query_utils import Prefetch


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


class ProductService:

    @staticmethod
    async def create_product(manufacturer_name: str, product_name: str, product_standard: str, product_approval: str):
        manufacturer = await Manufacturer.get_or_none(name=manufacturer_name)
        if not manufacturer:
            raise abort(404)
        product = await Product.create(name=product_name, standard=product_standard, approval=product_approval, manufacturer=manufacturer)
        return product

    @ staticmethod
    async def select_products():
        products = await Product.all().prefetch_related('manufacturer')
        return products

    @ staticmethod
    async def select_product_by_id(id: int):
        product = await Product.get_or_none(id=id).prefetch_related('manufacturer')
        if not product:
            raise abort(404)
        return product

    @ staticmethod
    async def select_distinct_products_by_manufacturer(manufacturer_name: str):
        products = await Product.all().prefetch_related(Prefetch('manufacturer', queryset=Manufacturer.filter(name=manufacturer_name))).distinct()
        return products

    @ staticmethod
    async def select_standards_by_manufacturer_and_product(manufacturer_name: str, product_name: str):
        products = await Product.filter(name=product_name).order_by('standard').prefetch_related(Prefetch('manufacturer', queryset=Manufacturer.filter(name=manufacturer_name)))
        return [product.standard for product in products]

    @ staticmethod
    async def patch_product(id: int, manufacturer_name: str, product_name: str, product_standard: str, product_approval: str):
        manufacturer = await Manufacturer.get_or_none(name=manufacturer_name)
        if not manufacturer:
            raise abort(404)
        await Product.select_for_update().get(id=id).update(name=product_name, standard=product_standard, approval=product_approval, manufacturer=manufacturer)
        product = await Product.get(id=id).prefetch_related('manufacturer')
        return product


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
