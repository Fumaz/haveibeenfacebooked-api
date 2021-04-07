from sanic import Sanic, json, text
from sanic.exceptions import NotFound, ServerError

from .db import Account

app = Sanic(__name__)


@app.exception(NotFound)
async def not_found(_, __):
    return json(dict(ok=True, message='Invalid endpoint.'), status=404)


@app.exception(ServerError)
async def internal_server_error(_, __):
    return json(dict(ok=False, message='Internal Server Error.'), status=500)


@app.exception(Exception)
async def default_error_handler(_, __):
    return json(dict(ok=False, message='What are you doing?'), status=500)


@app.post('/search')
async def search(request):
    phone_number = request.form.get('phone_number', None)
    email_address = request.form.get('email_address', None)

    if not (phone_number or email_address):
        return json(
            dict(ok=False, reason='arguments', message='Phone number or email address required'),
            status=200
        )

    if phone_number and len(phone_number) != 64:
        return json(
            dict(ok=False, reason='arguments', message='Phone number must be hashed in SHA256'),
            status=200
        )

    if not (account := await Account.fetch(phone_number=phone_number, email_address=email_address)):
        return json(dict(ok=True, found=False, data={}), status=200)

    return json(dict(ok=True, found=True, data=account.dictize()), status=200)


@app.middleware('response')
async def add_headers(_, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'


@app.get('/loaderio-d029151933cbc7cbc62e62092d5cfb86.html')
async def verification(request):
    return text('loaderio-d029151933cbc7cbc62e62092d5cfb86')


def run():
    app.run(host='127.0.0.1', port=5000, debug=True)
