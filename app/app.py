#!/usr/bin/env python
# coding: utf-8

import os
import subprocess

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast
from sqlalchemy.sql import text


app = Flask(__name__)

app.config['DB_DIRECTORY'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database')
app.config['DB_7Z_PATH'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database', 'permission_db.7z')
app.config['DB_PATH'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database', 'permission_db.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DB_PATH']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


declared_permissions = db.Table('declared_permissions', db.metadata,
                                db.Column('apk_id', db.String(32),
                                          db.ForeignKey('apks.md5'), primary_key=True),
                                db.Column('permission_id', db.Integer,
                                          db.ForeignKey('permissions.id'), primary_key=True))

required_and_used_permissions = db.Table('required_and_used_permissions', db.metadata,
                                         db.Column('apk_id', db.String(32),
                                                   db.ForeignKey('apks.md5'), primary_key=True),
                                         db.Column('permission_id', db.Integer,
                                                   db.ForeignKey('permissions.id'), primary_key=True))

required_but_not_used_permissions = db.Table('required_but_not_used_permissions', db.metadata,
                                             db.Column('apk_id', db.String(32),
                                                       db.ForeignKey('apks.md5'), primary_key=True),
                                             db.Column('permission_id', db.Integer,
                                                       db.ForeignKey('permissions.id'), primary_key=True))

not_required_but_used_permissions = db.Table('not_required_but_used_permissions', db.metadata,
                                             db.Column('apk_id', db.String(32),
                                                       db.ForeignKey('apks.md5'), primary_key=True),
                                             db.Column('permission_id', db.Integer,
                                                       db.ForeignKey('permissions.id'), primary_key=True))


class Apk(db.Model):

    __tablename__ = 'apks'

    md5 = db.Column(db.String(32), primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    source = db.Column(db.String(24), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    risk = db.Column(db.Float, nullable=False)

    declared_permissions = db.relationship('Permission', secondary=declared_permissions,
                                           backref=db.backref('app_declaring',
                                                              lazy='dynamic'))

    required_and_used_permissions = db.relationship('Permission', secondary=required_and_used_permissions,
                                                    backref=db.backref('app_requiring_and_using',
                                                                       lazy='dynamic'))

    required_but_not_used_permissions = db.relationship('Permission', secondary=required_but_not_used_permissions,
                                                        backref=db.backref('app_requiring_but_not_using',
                                                                           lazy='dynamic'))

    not_required_but_used_permissions = db.relationship('Permission', secondary=not_required_but_used_permissions,
                                                        backref=db.backref('app_not_requiring_but_using',
                                                                           lazy='dynamic'))

    def __repr__(self):
        return '<Apk (md5="{0}", name="{1}", risk="{2}")>'.format(self.md5, self.name, self.risk)


class Permission(db.Model):

    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Permission (name="{0}")>'.format(self.name)


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
             list(map(lambda x: {'cat': 'Declared', 'name': x.name}, apk.declared_permissions)) +
             list(map(lambda x: {'cat': 'Required and Used', 'name': x.name}, apk.required_and_used_permissions)) +
             list(map(lambda x: {'cat': 'Required but Not Used', 'name': x.name}, apk.required_but_not_used_permissions)) +
             list(map(lambda x: {'cat': 'Not Required but Used', 'name': x.name}, apk.not_required_but_used_permissions))]
    }

    return make_response(jsonify(response))


if __name__ == '__main__':
    setup_app()
    app.run(debug=True)
