import json
import time
import pymongo
import sys
import urllib.parse
import base64
import functools

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules/rest_api_controller")

sys.path.append("pytavia_modules/authentication") 
sys.path.append("pytavia_modules/registration") 

# adding comments
from pytavia_stdlib import utils
from pytavia_core import database
from pytavia_core import config
from pytavia_core import model
from pytavia_stdlib import idgen

from rest_api_controller import authenticaton
from rest_api_controller import taxpayer_registration
from rest_api_controller import map_regency
from rest_api_controller import map_district
from rest_api_controller import map_village

from registration import registration_taxpayer
from authentication import auth, dashboard
##########################################################

from flask import request
from flask import render_template
from flask import Flask, redirect, session, url_for

from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError

#
# Main app configurations
#
app = Flask(__name__, config.G_STATIC_URL_PATH)
csrf = CSRFProtect(app)
app.secret_key = config.G_FLASK_SECRET
app.db_update_context, app.db_table_fks = model.get_db_table_paths(model.db)


########################## CALLBACK  ###################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            session.clear()
            return redirect(url_for("login_view"))
        return func(*args, **kwargs)

    return secure_function

def login_required_api(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("signout"))
        return func(*args, **kwargs)

    return secure_function
# end def

# def
@app.route("/", methods=["GET"])
def signin_view():
    params = request.args.to_dict()
    response = auth.auth(app).signin( params )
    return response
# end def

# def
@app.route("/login", methods=["GET"])
def login_view():
    params = request.args.to_dict()
    response = auth.auth(app).signin( params )
    return response
# end def

# def
@app.route("/signup", methods=["GET"])
@login_required
def signup_view():
    params = request.args.to_dict()
    response = auth.auth(app).signup( params )
    return response
# end def

# def
@app.route("/logout", methods=["GET"])
def logout_view():
    params = request.args.to_dict()
    response = auth.auth(app).signout( params )
    return response
# end def

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard_view():
    params = request.args.to_dict()
    response = dashboard.dashboard(app).process( params )
    return response
# end def

@app.route("/taxpayer-registration", methods=["GET"])
@login_required
def registration():
    params = request.args.to_dict()
    response = registration_taxpayer.registration_taxpayer(app).process( params )
    return response
# end def

@app.route("/taxpayer-registration/<string:id>/edit", methods=["GET"])
@login_required
def edit_registration(id):
    params = request.args.to_dict()
    response = registration_taxpayer.registration_taxpayer(app).edit( params, id )
    return response
# end def

@app.route("/taxpayer-registration/create", methods=["GET"])
@login_required
def create_registration():
    params = request.args.to_dict()
    response = registration_taxpayer.registration_taxpayer(app).create( params )
    return response
# end def


########################## CALLBACK API ###################################
@app.route("/v1/api/signin", methods=["POST"])
def signin():
    params = request.args.to_dict()
    response = authenticaton.authenticaton(app).signin(params)
    return response.json_v1()

@app.route("/v1/api/signup", methods=["POST"])
def signup():
    params = request.args.to_dict()
    response = authenticaton.authenticaton(app).signup(params)
    return response.json_v1()

@app.route("/v1/api/signout", methods=["GET"])
def signout():
    params = request.args.to_dict()
    response = authenticaton.authenticaton(app).signout(params)
    return response.json_v1()

@app.route("/v1/api/taxpayer-registration", methods=["GET"])
@login_required_api
def lists_taxpayer_registration():
    params = request.args.to_dict()
    response = taxpayer_registration.taxpayer_registration(app).lists(params)
    return response.json_datatable()

@app.route("/v1/api/taxpayer-registration/<string:registration_id>", methods=["GET"])
@login_required_api
def get_taxpayer_registration(registration_id):
    params = request.args.to_dict()
    response = taxpayer_registration.taxpayer_registration(app).get(params, registration_id)
    return response.json_v1()

@app.route("/v1/api/taxpayer-registration", methods=["POST"])
@login_required_api
def store_taxpayer_registration():
    params = request.args.to_dict()
    response = taxpayer_registration.taxpayer_registration(app).store(params)
    return response.json_v1()

@app.route("/v1/api/taxpayer-registration", methods=["PUT"])
@login_required_api
def update_taxpayer_registration():
    params = request.args.to_dict()
    response = taxpayer_registration.taxpayer_registration(app).update(params)
    return response.json_v1()

@app.route("/v1/api/taxpayer-registration/<string:registration_id>", methods=["DELETE"])
@login_required_api
def delete_taxpayer_registration(registration_id):
    params = request.args.to_dict()
    response = taxpayer_registration.taxpayer_registration(app).destroy(params, registration_id)
    return response.json_v1()

@app.route("/v1/api/regency/lists/<int:province_id>", methods=["GET"])
def map_regency_lists(province_id):
    params = request.args.to_dict()
    response = map_regency.map_regency(app).lists(params, province_id)
    return response.json_v1()

@app.route("/v1/api/district/lists/<int:regency_id>", methods=["GET"])
def map_district_lists(regency_id):
    params = request.args.to_dict()
    response = map_district.map_district(app).lists(params, regency_id)
    return response.json_v1()

@app.route("/v1/api/village/lists/<int:district_id>", methods=["GET"])
def map_village_lists(district_id):
    params = request.args.to_dict()
    response = map_village.map_village(app).lists(params, district_id)
    return response.json_v1()
# end def