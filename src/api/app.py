import logging
from datetime import timedelta, datetime

from flask import Flask, request, jsonify

from .models import *

app = Flask(__name__)
app.logger.disabled = True

log = logging.getLogger('werkzeug')
log.disabled = True

cooldown = {}


@app.route('/search', methods=['GET', 'POST'])
def search():
    ip_address = request.headers.get('CF-Connecting-IP', None)
    if request.method == 'POST':
        phone_number = request.values.get('phone_number', None)
    else:
        phone_number = request.args.get('phone_number', None)

    if not ip_address:
        Stats.increment('invalid')
        return jsonify(ok=False, reason='ip', message='Invalid IP Address. (Are you a bot?)')

    if cooldown.get(ip_address, datetime.min) > datetime.now():
        Stats.increment('invalid')
        return jsonify(ok=False, reason='flood', message='Slow down! Too many requests.')

    if not phone_number:
        Stats.increment('invalid')
        return jsonify(ok=False, reason='arguments', message='Invalid Phone Number.')

    cooldown[ip_address] = datetime.now() + timedelta(seconds=2)

    with db_session:
        Stats.increment('requests')
        account = Account.find(phone_number=phone_number)

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
