from flask import Flask, render_template, redirect, url_for, request, session, Response, make_response, jsonify
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
from flask import current_app as app
import xmlrpc.client
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from .odoohelper import OdooHelper

odoo = OdooHelper(app)

@app.route('/', methods=["GET"])
def index():
    return "API Version 1.0"

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200


@app.route('/login/')
def login():   
    try:
        auth = request.authorization
        url = 'http://' + app.config['RDM_SERVER'] + ':' + app.config['RDM_PORT']
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        email = auth.username
        password = auth.password
        print(email)
        print(app.config['RDM_DB_NAME'])
        print(app.config['RDM_APP_EMAIL'])
        print(app.config['RDM_APP_PASSWORD'])
        uid = common.authenticate(app.config['RDM_DB_NAME'], app.config['RDM_APP_EMAIL'], app.config['RDM_APP_PASSWORD'], {})
        if (uid == False):
            return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
        ret = {
            'access_token': create_access_token(identity=email),
            'refresh_token': create_refresh_token(identity=email)
        }
        return jsonify(ret), 200
    except Exception as e:
        print(str(e))
        #return jsonify({'error': True, 'message': str(e), 'uid': False})
        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@app.route('/api/v1.0/tenant_categories/<int:offset>/<int:limit>/', methods=['POST'])
@jwt_required
def get_tenant_categories(offset, limit):
    return jsonify(
        'rdm.tenant.category',
        ['name'],
        offset,
        limit
    )
    
@app.route('/api/v1.0/tenant_by_categories/<int:category_id>/<int:offset>/<int:limit>/', methods=['POST'])
@jwt_required
def get_tenant_by_categories(category_id, offset, limit):
    return jsonify(odoo.get_pagination_search('rdm.tenant',
                                              ['name'], 
                                              [[['category','=', category_id]]], 
                                              offset, 
                                              limit))
    
@app.route('/api/v1.0/tenant/<int:tenant_id>/', methods=['POST'])
@jwt_required
def get_tenant(tenant_id):
    return jsonify(odoo.get_id('rdm.tenant', tenant_id, ['name']))

@app.route('/api/v1.0/rewards/<int:offset>/<int:limit>/', methods=['POST'])
@jwt_required
def get_rewards(offset,limit):
    return odoo.get_pagination('rdm.reward',
                               ['name','point'],
                               offset,
                               limit)

@app.route('/api/v1.0/promos/<int:offset>/<int:limit>/', methods=['POST'])
@jwt_required
def get_promos(offset, limit):
    result = odoo.get_list('rdm.schemas',['name'])
    return jsonify(result)
    
       
@app.route('/api/v1.0/transaction_by_customer/<int:customer_id>/<int:offset>/<int:limit>/', methods=['POST'])
@jwt_required
def get_(customer_id, offset, limit):
    return jsonify(
        odoo.get_pagination_search('rdm.trans',
                                   ['name'], 
                                   [[['customer_id','=', customer_id]]], 
                                   offset, 
                                   limit)
        )
 
@app.route('/api/v1.0/my_profile/<int:customer_id>/', methods=['GET'])
@jwt_required
def get_my_profile(customer_id):
    return jsonify(
        odoo.get_id('rdm.customer',customer_id, ['name'])
    )
    
    
@app.route('/api/v1.0/banners/<int:offset>/<int:limit>/', methods=['GET'])
@jwt_required
def get_banners(offset=0,limit=10):
    return jsonify(odoo.get_pagination(
                    'rdm.mobile.banner',
                    ['name'],
                    offset,
                    limit
                )
    )