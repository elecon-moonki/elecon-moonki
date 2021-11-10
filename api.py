import os
from sanic import Sanic
from sanic.exceptions import abort
from sanic.response import json, file
from sanic import Blueprint
from tortoise.contrib.sanic import register_tortoise
import urllib.parse
from apis.manufacturer import manufacturer
from apis.product import product
from apis.shipping import shipping

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

api = Blueprint.group(shipping, product, manufacturer, url_prefix='/api')
app = Sanic('elecon Shipping api')
app.config.BASE_DIR = BASE_DIR
app.blueprint(api)

app.static('/static/approval', f'{BASE_DIR}/static/approval', name='approval')
app.static('/static/receipt', f'{BASE_DIR}/static/approval', name='receipt')


USER = 'moonki'
PASSWORD = urllib.parse.quote_plus('moonki12#')
HOST = '127.0.0.1'
DATABASE = 'elecon_shipping'

register_tortoise(
    app, db_url=f'mysql://{USER}:{PASSWORD}@{HOST}:3306/{DATABASE}', modules={'models': ['models.manufacturer', 'models.shipping', 'models.product', 'models.site']}, generate_schemas=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True,
            access_log=True, auto_reload=True)
