from flask             import request
from flask             import jsonify

from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import bulk_db_multi

# adding comments

class map_village:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def lists(self, app, district_id):
        from pytavia_core import helper
        row = []

        row.append({
            'id'    : 0,
            'name'  : 'PILIH KELURAHAN'
        })

        regency = self.mgdDB.map_village.find({'district.code' : str(district_id)}, {"code" : 1, "name" : 1})

        for rows in regency:
            row.append({
                'id'    : rows["code"],
                'name'  : rows["code"] + " - " + rows["name"]
            })
        

        response = helper.response_msg("PROCESS_SUCCESS", "List Village", row, 200)
        return response

