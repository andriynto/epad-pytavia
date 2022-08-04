import json
import time
import pymongo
import sys
import pprint
import urllib.request

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")
sys.path.append("iso")


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

    def iso(self, param):
        import      iso8583
        from iso    import protocol8583

        incomingMessage = '0151ISO00500001702007238400108818000166274860024132493360000000000000000080407172406186714172408047016040117220804061701024132490211209411011001222161  360'

        provider = 'bnksumut'
        message  = protocol8583.protocol8583.process(provider, incomingMessage.encode('utf-8'), encodeType = 'raw')

        pprint.pp(message)

        response = render_template(
            "auth/blank.html", message = json.dumps(message)
        )

        return response