from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from services.product import ProductService as Product
import os
import aiofiles
from sanic.log import logger

product = Blueprint('product api', url_prefix='/product')


@product.route('/<id>', methods=['GET', 'PATCH'])
async def get_patch_product(request, id):
    if request.method == 'GET':
        try:
            product = await Product.select_product_by_id(id=id)
        except:
            raise abort(500)

        return json({'id': product.id, 'name': product.name, 'standard': product.standard, 'approval': product.approval, 'manufacturer_name': product.manufacturer.name}, status=200)
    else:
        try:
            manufacturer_name = request.form.get('manufacturer_name')
            product_name = request.form.get('product_name')
            product_standard = request.form.get('product_standard')
            approval_ext = os.path.splitext(
                request.files['product_approval'][0].name)[-1]
            product_approval = f'{manufacturer_name}_{product_name}_{product_standard}{approval_ext}'
            async with aiofiles.open(f'{request.app.config.BASE_DIR}/static/approval/{product_approval}', 'wb') as f:
                await f.write(request.files['product_approval'][0].body)
        except:
            raise RuntimeError(
                'Could not get arguments [manufacturer_name, product_name, product_standard, product_approval]')
        else:
            product_approval_url = f'/static/approval/{product_approval}'
            try:
                product = await Product.patch_product(id=id, manufacturer_name=manufacturer_name, product_name=product_name,
                                                      product_standard=product_standard, product_approval=product_approval_url)
            except:
                raise abort(500)

        return json({'id': product.id, 'name': product.name, 'standard': product.standard, 'approval': product.approval, 'manufacturer_name': product.manufacturer.name}, status=200)


@product.route('/', methods=['GET', 'POST'])
async def get_products(request):
    if request.method == 'GET':
        if request.query_string:
            try:
                manufacturer_name = request.args.get('manufacturer_name')
            except:
                raise RuntimeError(
                    'Could not get argument [manufacturer_name]')
            else:
                try:
                    products = await Product.select_distinct_products_by_manufacturer(
                        manufacturer_name=manufacturer_name)
                except:
                    raise abort(500)

                return json([{'id': product.id, 'name': product.name, 'standard': product.standard, 'approval': product.approval,
                              'manufacturer_name': product.manufacturer.name} for product in products], status=200)
        else:
            try:
                products = await Product.select_products()
            except:
                raise abort(500)

            return json([{'id': product.id, 'name': product.name, 'standard': product.standard, 'approval': product.approval,
                          'manufacturer_name': product.manufacturer.name} for product in products], status=200)
    else:
        try:
            manufacturer_name = request.form.get('manufacturer_name')
            product_name = request.form.get('product_name')
            product_standard = request.form.get('product_standard')
            approval_ext = os.path.splitext(
                request.files['product_approval'][0].name)[-1]
            product_approval = f'{manufacturer_name}_{product_name}_{product_standard}{approval_ext}'
            async with aiofiles.open(f'{request.app.config.BASE_DIR}/static/approval/{product_approval}', 'wb') as f:
                await f.write(request.files['product_approval'][0].body)
        except Exception as e:
            logger.error(str(e))
            abort(500)
        else:
            product_approval_url = f'/static/approval/{product_approval}'
            try:
                product = await Product.create_product(manufacturer_name=manufacturer_name, product_name=product_name, product_standard=product_standard, product_approval=product_approval_url)
            except:
                abort(500)
            return json({'name': product.name, 'standard': product.standard, 'approval': product.approval, 'manufacturer_name': product.manufacturer.name}, status=200)


@product.route('/standard', methods=['GET'])
async def get_standards(request):
    try:
        product_name = request.args.get('product_name')
        manufacturer_name = request.args.get('manufacturer_name')
    except:
        raise RuntimeError(
            'Could not get get arguments [product_name, manufacturer_name]')
    else:
        try:
            standards = await Product.select_standards_by_manufacturer_and_product(
                manufacturer_name=manufacturer_name, product_name=product_name)
        except:
            raise abort(500)

    return json({'standard': standards}, status=200)
