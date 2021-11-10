from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from services import ShippingService as Shipping
from datetime import datetime
import os
import aiofiles

shipping = Blueprint('shipping api', url_prefix='/shipping')


@shipping.route('/', methods=['GET', 'POST'])
async def get_post_shipping(request):
    if request.method == 'POST':
        try:
            due_datetime = request.json.get('due_datetime')
            site_address = request.json.get('site_address')
            site_phone_number = request.json.get('site_phone_number')
            manufacturer_name = request.json.get('manufacturer_name')
            manufacturer_manager = request.json.get('manufacturer_manager')
            manufacturer_phone_number = request.json.get(
                'manufacturer_phone_number')
            manufacturer_address = request.json.get('manufacturer_address')
            products = request.json.get('products')
            vehicle_number = request.json.get('vehicle_number')
            vehicle_type = request.json.get('vehicle_type')
            driver = request.json.get('driver')
            driver_phone_number = request.json.get('driver_phone_number')
        except:
            raise abort(400)
        else:
            try:
                shipping = await Shipping.create_shipping(due_datetime=due_datetime, site_address=site_address, site_phone_number=site_phone_number, manufacturer_name=manufacturer_name, manufacturer_address=manufacturer_address,
                                                          manufacturer_manager=manufacturer_manager, manufacturer_phone_number=manufacturer_phone_number, products=products, vehicle_number=vehicle_number, vehicle_type=vehicle_type, driver=driver, driver_phone_number=driver_phone_number)
            except:
                raise abort(500)

            return json({'id': shipping.id, 'due_datetime': shipping.due_datetime.strftime('%Y년 %m월 %d일 %H시 %M분'), 'site_address': shipping.site.address, 'site_phone_number': shipping.site.phone_number, 'manufacturer_name': shipping.manufacturer_name,
                         'manufacturer_address': shipping.manufacturer_address, 'manufacturer_manager': shipping.manufacturer_manager, 'manufacturer_phone_number': shipping.manufacturer_phone_number,
                         'products': shipping.products, 'vehicle_number': shipping.vehicle_number, 'vehicle_type': shipping.vehicle_type, 'driver': shipping.driver, 'shipping_status': shipping.shipping_status,
                         'driver_phone_number': shipping.driver_phone_number}, status=200)
    else:
        try:
            shippings = await Shipping.select_shippings()
        except:
            raise abort(500)

        return json([{'id': shipping.id, 'due_datetime': shipping.due_datetime.strftime('%Y년 %m월 %d일 %H시 %M분'), 'site_address': shipping.site.address, 'site_phone_number': shipping.site.phone_number, 'manufacturer_name': shipping.manufacturer_name,
                      'manufacturer_address': shipping.manufacturer_address, 'manufacturer_manager': shipping.manufacturer_manager, 'manufacturer_phone_number': shipping.manufacturer_phone_number,
                      'products': shipping.products, 'vehicle_number': shipping.vehicle_number, 'vehicle_type': shipping.vehicle_type, 'driver': shipping.driver, 'shipping_status': shipping.shipping_status,
                      'driver_phone_number': shipping.driver_phone_number} for shipping in shippings], status=200)


@shipping.route('/<id>/status', methods=['POST'])
async def post_status(request, id):
    try:
        shipping_status = request.form.get('shipping_status')
        receipt = request.files.get('receipt', None)
        if receipt:
            receipt_ext = os.path.splitext(receipt.name)[-1]
            receipt_filename = f'{id}{receipt_ext}'
            async with aiofiles.open(f'{request.app.config.BASE_DIR}/static/receipt/{receipt_filename}', 'wb') as f:
                await f.write(receipt.body)
    except:
        raise abort(400)
    else:
        try:
            receipt_url = f'/static/receipt/{receipt_filename}'
            shipping = await Shipping.patch_status(
                id=id, shipping_status=shipping_status, receipt=receipt_url)
        except:
            raise abort(500)

        return json({'id': shipping.id, 'due_datetime': shipping.due_datetime.strftime('%Y년 %m월 %d일 %H시 %M분'), 'site_address': shipping.site.address, 'site_phone_number': shipping.site.phone_number, 'manufacturer_name': shipping.manufacturer_name,
                    'manufacturer_address': shipping.manufacturer_address, 'manufacturer_manager': shipping.manufacturer_manager, 'manufacturer_phone_number': shipping.manufacturer_phone_number,
                     'products': shipping.products, 'vehicle_number': shipping.vehicle_number, 'vehicle_type': shipping.vehicle_type, 'driver': shipping.driver, 'shipping_status': shipping.shipping_status,
                     'driver_phone_number': shipping.driver_phone_number}, status=200)


@shipping.route('/<id>', methods=['GET', 'PATCH'])
async def get_patch_shipping(request, id):
    if request.method == 'GET':
        try:
            shipping = await Shipping.select_shipping(id=id)
        except:
            raise abort(500)
        return json({'due_datetime': shipping.due_datetime.strftime('%Y년 %m월 %d일 %H시 %M분'), 'site_address': shipping.site.address, 'site_phone_number': shipping.site.phone_number, 'manufacturer_name': shipping.manufacturer_name,
                     'manufacturer_address': shipping.manufacturer_address, 'manufacturer_manager': shipping.manufacturer_manager, 'manufacturer_phone_number': shipping.manufacturer_phone_number,
                     'products': shipping.products, 'vehicle_number': shipping.vehicle_number, 'vehicle_type': shipping.vehicle_type, 'driver': shipping.driver, 'shipping_status': shipping.shipping_status,
                     'driver_phone_number': shipping.driver_phone_number}, status=200)
    else:
        try:
            due_datetime = request.json.get('due_datetime')
            site_address = request.json.get('site_address')
            site_phone_number = request.json.get('site_phone_number')
            manufacturer_name = request.json.get('manufacturer_name')
            manufacturer_manager = request.json.get('manufacturer_manager')
            manufacturer_phone_number = request.json.get(
                'manufacturer_phone_number')
            manufacturer_address = request.json.get('manufacturer_address')
            products = request.json.get('products')
            vehicle_number = request.json.get('vehicle_number')
            vehicle_type = request.json.get('vehicle_type')
            driver = request.json.get('driver')
            driver_phone_number = request.json.get('driver_phone_number')
        except:
            raise abort(400)
        else:
            try:
                shipping = await Shipping.patch_shipping(id=id, due_datetime=due_datetime, site_address=site_address, site_phone_number=site_phone_number, manufacturer_name=manufacturer_name, manufacturer_manager=manufacturer_manager,
                                                         manufacturer_phone_number=manufacturer_phone_number, products=products, manufacturer_address=manufacturer_address, vehicle_number=vehicle_number, vehicle_type=vehicle_type, driver=driver, driver_phone_number=driver_phone_number)
            except:
                raise abort(500)
            return json({'id': shipping.id, 'due_datetime': shipping.due_datetime.strftime('%Y년 %m월 %d일 %H시 %M분'), 'site_address': shipping.site.address, 'site_phone_number': shipping.site.phone_number, 'manufacturer_name': shipping.manufacturer_name,
                         'manufacturer_address': shipping.manufacturer_address, 'manufacturer_manager': shipping.manufacturer_manager, 'manufacturer_phone_number': shipping.manufacturer_phone_number,
                         'products': shipping.products, 'vehicle_number': shipping.vehicle_number, 'vehicle_type': shipping.vehicle_type, 'driver': shipping.driver, 'shipping_status': shipping.shipping_status,
                         'driver_phone_number': shipping.driver_phone_number}, status=200)
