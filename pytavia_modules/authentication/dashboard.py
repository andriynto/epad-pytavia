import sys
import urllib.request

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template

class dashboard:

    def __init__(self, app):
        self.webapp = app

    def process(self, param):
        response = render_template(
            "dashboard.html"
        )

        return response