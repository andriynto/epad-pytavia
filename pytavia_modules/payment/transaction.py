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

class transaction:

    def __init__(self, app):
        self.webapp = app

    def process(self, param):
        from datetime import datetime
        now = datetime.now()

        transmission_datetime = now.strftime("%m%d%H%M%S")
        date_transaction = now.strftime("%m%d")
        time_transaction = now.strftime("%H%M%S")

        response = render_template(
            "payment/index.html",
            transmission_datetime = transmission_datetime,
            time_transaction = time_transaction,
            date_transaction = date_transaction
        )

        return response