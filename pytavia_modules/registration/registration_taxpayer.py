import json
import time
import pymongo
import sys
import urllib.parse
import base64
import traceback
import random
import urllib.request
import io
import requests
import hashlib

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template
from flask             import request

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

class registration_taxpayer:
    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app

    def process(self, param):
        # taxpayer = self.mgdDB.taxpayer_registration.find({})

        # ALL_DATA     = list( taxpayer )

        response = render_template(
            "registration/taxpayer/index.html"
        )

        return response

    def create(self, param):
        response = render_template(
            "registration/taxpayer/create.html"
        )

        return response

    def edit(self, param, id):
        response = render_template(
            "registration/taxpayer/edit.html", id = id
        )

        return response
# end class