import logging
from datetime import timedelta

from flask import Flask, request, jsonify

from .models import *

app = Flask(__name__)
app.logger.disabled = True

log = logging.getLogger('werkzeug')
log.disabled = True

cooldown = {}


@app.route('/search')
def search():
    ip_address = request.headers.get('CF-Connecting-IP', None)
    phone_number = request.args.get('phone_number', None)

    if not ip_address:
        Stats.add_invalid()
        return jsonify(ok=False, reason='ip', message='Invalid IP Address. (Are you a bot?)')

    if cooldown.get(ip_address, datetime.min) > datetime.now():
        Stats.add_invalid()
        return jsonify(ok=False, reason='flood', message='Slow down! Too many requests.')

    if not phone_number or not phone_number.startswith('+'):
        Stats.add_invalid()
        return jsonify(ok=False, reason='arguments', message='Invalid Phone Number.')

    try:
        phone_number = int(phone_number.replace(' ', ''))
    except ValueError:
        Stats.add_invalid()
        return jsonify(ok=False, reason='arguments', message='Invalid Phone Number.')

    cooldown[ip_address] = datetime.now() + timedelta(seconds=2)

    with db_session:
        account = SQLiteAccount.find(phone_number=phone_number)

        stats = Stats.get(name='requests')
        stats.value += 1
        commit()

        if not account:
            return jsonify(ok=True, found=False, data={})

        return jsonify(ok=True, found=True, data=account.dictize())


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def run():
    print('Running Flask', flush=True)
    app.run(host='0.0.0.0')
