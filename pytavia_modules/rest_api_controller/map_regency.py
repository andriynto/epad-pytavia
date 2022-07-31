from flask             import request
from flask             import jsonify

from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import bulk_db_multi

# adding comments

class map_regency:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def lists(self, app, province_id):
        from pytavia_core import helper
        # data = request.get_json()
        # province_id = data.get('province_id')
        row = []

        row.append({
            'id'    : 0,
            'name'  : 'PILIH KABUPATEN/KOTA'
        })

        provinces = self.mgdDB.map_regency.find({'province' : str(province_id)}, {"code" : 1, "name" : 1})

        for rows in provinces:
            row.append({
                'id'    : rows["code"],
                'name'  : rows["code"] + " - " + rows["name"]
            })
        

        response = helper.response_msg("PROCESS_FAILED", "Entity Error", row, 200)
        return response

