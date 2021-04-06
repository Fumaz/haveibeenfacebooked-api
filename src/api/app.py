from datetime import timedelta, datetime

from flask import Flask, request, jsonify

from .models import *

app = Flask(__name__)
cooldown = {}


@app.errorhandler(404)
def not_found():
    return jsonify(ok=True, message='What do you think you\'re doing?')


@app.route('/search', methods=['GET', 'POST'])
def search():
    phone_number = (request.values if request.method == 'POST' else request.args).get('phone_number', None)

    # if not ip_address:
        # return jsonify(ok=False, reason='ip', message='Invalid IP Address. (Are you a bot?)')

    #if cooldown.get(ip_address, datetime.min) > datetime.now():
    #    return jsonify(ok=False, reason='flood', message='Slow down! Too many requests.')

    if not phone_number:
        return jsonify(ok=False, reason='arguments', message='Invalid Phone Number.')

    # cooldown[ip_address] = datetime.now() + timedelta(seconds=3)

    with db_session:
        account = Account.find(phone_number=phone_number)

        if not account:
            return jsonify(ok=True, found=False, data={})

        return jsonify(ok=True, found=True, data=account.dictize())


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://haveibeenfacebooked.com'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    return response


def run():
    print('Running Flask', flush=True)
    app.run(host='0.0.0.0')
