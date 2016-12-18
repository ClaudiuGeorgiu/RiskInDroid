#!/usr/bin/env python
# coding: utf-8

import os
import subprocess

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import request
from sqlalchemy import cast
from sqlalchemy.sql import text

from RiskInDroid import RiskInDroid
from model import db, Apk


app = Flask(__name__)

app.config['DB_DIRECTORY'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database')
app.config['DB_7Z_PATH'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database', 'permission_db.7z')
app.config['DB_PATH'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database', 'permission_db.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DB_PATH']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def setup_app():
    # Check if the database file is already extracted from the archive, otherwise extract it.
    if not os.path.isfile(app.config['DB_PATH']):
        instruction = '7z x "{0}" -o"{1}"'.format(app.config['DB_7Z_PATH'], app.config['DB_DIRECTORY'])
        subprocess.run(instruction)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/apks', methods=['GET'])
def get_apks():

    query = Apk.query

    if request.args.get('sort') and request.args.get('sort_dir'):
        query = query.order_by(text('{0} {1}'.format(request.args.get('sort'), request.args.get('sort_dir'))))

    if request.args.get('namefil'):
        fil = request.args.get('namefil').replace('%', '\\%').replace('_', '\\_')
        query = query.filter(Apk.name.ilike('%{0}%'.format(fil), '\\'))

    if request.args.get('md5fil'):
        fil = request.args.get('md5fil').replace('%', '\\%').replace('_', '\\_')
        query = query.filter(Apk.md5.ilike('%{0}%'.format(fil), '\\'))

    if request.args.get('riskfil'):
        fil = request.args.get('riskfil').replace('%', '\\%').replace('_', '\\_')
        query = query.filter(cast(Apk.risk, db.String).ilike('%{0}%'.format(fil), '\\'))

    pag = query.paginate()

    item_list = []

    for item in pag.items:
        item_list.append({
            'name': item.name,
            'md5': item.md5,
            'risk': item.risk
        })

    response = {
        'current_page': pag.page,
        'last_page': pag.pages,
        'data': item_list
    }

    return make_response(jsonify(response))


@app.route('/details', methods=['GET'])
def get_app_details():

    md5 = request.args.get('md5')

    apk = Apk.query.get(md5)

    response = {
        'name': apk.name,
        'md5': apk.md5,
        'risk': apk.risk,
        'type': apk.type,
        'source': apk.source,
        'permissions':
            [val for val in
             list(map(lambda x: {'cat': 'Declared', 'name': x.name},
                      apk.declared_permissions)) +
             list(map(lambda x: {'cat': 'Required and Used', 'name': x.name},
                      apk.required_and_used_permissions)) +
             list(map(lambda x: {'cat': 'Required but Not Used', 'name': x.name},
                      apk.required_but_not_used_permissions)) +
             list(map(lambda x: {'cat': 'Not Required but Used', 'name': x.name},
                      apk.not_required_but_used_permissions))]
    }

    return make_response(jsonify(response))


@app.route('/rid', methods=['GET'])
def risk_in_droid():
    rid = RiskInDroid()

    rid.performance_analysis()

    return 'OK', 200


if __name__ == '__main__':
    db.init_app(app)
    setup_app()
    app.run()
