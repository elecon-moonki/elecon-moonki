from models.product import Product
from models.manufacturer import Manufacturer
from tortoise.query_utils import Prefetch
from sanic.exceptions import abort


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
