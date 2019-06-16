import requests
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# just a comment to test jenkins trigger
bp = Blueprint('generator', __name__, url_prefix='/')

host = "password-service:5000"


def call_password_service(host, pwd_len, special, numbers, uppercase):
    body = {}
    body["len"] = pwd_len
    body["special"] = special
    body["capital"] = uppercase
    body["numbers"] = numbers

    headers = {
        'Content-Type': "application/json"
    }
    try:
        pwd = requests.post("http://" + host, headers=headers, data=json.dumps(body))
        pwd_str = json.loads(pwd.text)["password"]
        return {'error': None, 'password': pwd_str}
    except requests.ConnectionError as e:
        return {'error': 'Could not connect to the host.', 'password': None}


@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        pwd_len = request.form.get('length')
        special = request.form.get('special')
        numbers = request.form.get('numbers')
        uppercase = request.form.get('uppercase')

        if special == 'on':
            special = True
        else:
            special = False
        if numbers == 'on':
            numbers = True
        else:
            numbers = False

        if uppercase == 'on':
            uppercase = True
        else:
            uppercase = False

        error = None

        if pwd_len is None:
            error = 'You must set password length'
            return render_template('generator.html', error=error)

        if int(pwd_len) <=0:
            error = 'Length cannot be less than or equal 0!'
            return render_template('generator.html', error=error)

        if error is None:
            password_response = call_password_service(host, pwd_len, special, numbers, uppercase)
            return render_template('generator.html', pwd=password_response['password'], error=password_response['error'])
        flash(error)

    return render_template('generator.html')
