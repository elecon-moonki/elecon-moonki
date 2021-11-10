from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from services import ManufacturerService as Manufacturer

manufacturer = Blueprint('manufacturer api', url_prefix='/manufacturer')


@manufacturer.route('/<id>', methods=['GET', 'PATCH'])
async def get_patch_manufacturer(request, id):
    if request.method == 'GET':
        try:
            manufacturer = await Manufacturer.select_manufacturer(id=id)
        except:
            raise abort(500)
        return json({'id': manufacturer.id, 'name': manufacturer.name, 'address': manufacturer.address, 'manager': manufacturer.manager, 'phone_number': manufacturer.phone_number}, status=200)
    else:
        try:
            manufacturer_name = request.json.get('manufacturer_name')
            manufacturer_address = request.json.get('manufacturer_address')
            manufacturer_manager = request.json.get('manufacturer_manager')
            manufacturer_phone_number = request.json.get(
                'manufacturer_phone_number')
        except:
            raise RuntimeError(
                'Could not get arguments [manufacturer_name, manufacturer_address, manufacturer_manager, manufacturer_phone_number]')
        else:
            try:
                manufacturer = await Manufacturer.patch_manufacturer(id=id, manufacturer_name=manufacturer_name, manufacturer_address=manufacturer_address,
                                                                     manufacturer_manager=manufacturer_manager, manufacturer_phone_number=manufacturer_phone_number)
            except:
                abort(500)
            return json({'id': manufacturer.id, 'name': manufacturer_name, 'address': manufacturer_address, 'manager': manufacturer_manager, 'phone_number': manufacturer_phone_number}, status=200)


@manufacturer.route('/', methods=['GET', 'POST'])
async def get_post_manufacturer(request):
    if request.method == 'GET':
        try:
            manufacturers = await Manufacturer.select_manufacturers()
        except:
            raise abort(500)

        return json([{'name': manufacturer.name, 'address': manufacturer.address, 'manager': manufacturer.manager,
                      'phone_number': manufacturer.phone_number}for manufacturer in manufacturers], status=200)
    else:
        try:
            manufacturer_name = request.json.get('manufacturer_name')
            manufacturer_address = request.json.get('manufacturer_address')
            manufacturer_manager = request.json.get('manufacturer_manager')
            manufacturer_phone_number = request.json.get(
                'manufacturer_phone_number')
        except:
            raise RuntimeError(
                'Could not get arguments [manufacturer_name, manufacturer_address, manufacturer_manager, manufacturer_phone_number]')
        else:
            try:
                manufacturer = await Manufacturer.create_manufacturer(manufacturer_name=manufacturer_name, manufacturer_address=manufacturer_address,
                                                                      manufacturer_manager=manufacturer_manager, manufacturer_phone_number=manufacturer_phone_number)
            except:
                abort(500)

            return json({'name': manufacturer.name, 'address': manufacturer.address, 'manager': manufacturer.manager, 'phone_number': manufacturer_phone_number}, status=200)
