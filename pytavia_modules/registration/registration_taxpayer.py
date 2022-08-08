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
import hashlib

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template

class registration_taxpayer:

    def __init__(self, app):
        self.webapp = app

    def process(self, param):
        response = render_template(
            "registration/taxpayer/index.html"
        )

        return response

    def create(self, param):
        response = render_template(
            "registration/taxpayer/create.html"
        )

        return response

    def show(self, param, id):
        response = render_template(
            "registration/taxpayer/show.html", id = id
        )

        return response

    def edit(self, param, id):
        response = render_template(
            "registration/taxpayer/edit.html", id = id
        )

        return response
# end class