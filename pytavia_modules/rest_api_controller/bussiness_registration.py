import sys

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template

class bussiness_registration:

    def __init__(self, app):
        self.webapp = app

    def add(self, param, id):
        response = render_template(
            "registration/bussiness/create.html", id = id
        )

        return response