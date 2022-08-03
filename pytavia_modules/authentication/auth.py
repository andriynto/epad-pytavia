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
from flask             import Flask, redirect, session, url_for

class auth:
    def __init__(self, app):
        self.webapp = app

    def signin(self, param):
        response = render_template(
            "auth/signin.html"
        )

        return response

    def signup(self, param):
        response = render_template(
            "auth/signup.html"
        )

        return response

    def signout(self, param):
        session.clear()
        return redirect(url_for("login_view"))