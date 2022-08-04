from collections       import namedtuple
from queue import Empty
from flask             import jsonify, request, url_for

from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import bulk_db_multi

# adding comments

class taxpayer_registration:

    mgdDB = database.get_db_conn(config.mainDB)

    # def
    def __init__(self, app):
        self.webapp = app
    # end def

    # def lists
    # Listing of the resource.
    def lists(self, params):
        from pytavia_core import helper

        limit = params.get('length')
        start = params.get('start')

        response = helper.response_msg(
            "LIST TAXPAYER SUCCESS",
            "", {},
            200
        )

        data = []
        filter_data = False

        if params.get('search[value]'):
            filter_data = True

        if filter_data == True:
            search = params.get('search[value]')

            self.mgdDB.taxpayer_registration.create_index([
                    ("name","text"),("identity_number","text")
                ]
            )

            taxpayer = self.mgdDB.taxpayer_registration.find({
                "status"    : {
                    "$in"   : ["Draft", "Reject"]
                },
                "archived_timestamp" : {
                    "$eq" : ""
                },
                "$text" : { "$search" : search },
            })
            
            total_data = taxpayer.count()
        else:
            taxpayer    = self.mgdDB.taxpayer_registration.find({
                "status"    : {
                    "$in"   : ["Draft", "Reject"]
                },
                "archived_timestamp" : {
                    "$eq" : ""
                }

            }).skip(int(start)).limit(int(limit)).sort([("date_record" , -1)])
            total_data  = self.mgdDB.taxpayer_registration.find({}).count()

        totalFiltered = total_data

        for rows in taxpayer:
            data.append({
                'id'                            : rows["pkey"],
                'status'                        : rows["status"],
                'register_transaction'          : rows["register_transaction"],
                'taxpayer_type'                 : rows["taxpayer_type"],
                'registration_number'           : rows["registration_number"],
                'identity_number'               : rows["identity_number"],
                'name'                          : rows["name"],
                'date_record'                   : rows['date_record'],
                'date_verification'             : rows['date_verification']
            })

        response.put( "data" ,  data )
        response.put( "draw" ,  int(params.get('draw')) )
        response.put( "recordsTotal" , int(totalFiltered) )
        response.put( "recordsFiltered" ,  int(totalFiltered) )

        return response
    #end def

    # def lists
    # Display the specified resource.
    def get(self, params, registration_id):
        from pytavia_core import helper
        from bson.objectid import ObjectId

        data = []
        taxpayer = self.mgdDB.taxpayer_registration.find_one({
            "pkey": registration_id,
            "archived_timestamp" : {
                "$eq" : ""
            }
        })

        employeeRecord       = self.mgdDB.employee.find_one({ "_id" : ObjectId(taxpayer['fk_record_by']['pkey'])})
        employeeVerification = self.mgdDB.employee.find_one({ "_id" : ObjectId(taxpayer['fk_verification_by']['pkey']) })

        data = {
            "status"                : taxpayer['status'],
            "registration_number"   : taxpayer['registration_number'],
            "name"                  : taxpayer['name'],
            'register_transaction'  : taxpayer['register_transaction'],
            'identity_number'       : taxpayer['identity_number'],
            'taxpayer_type'         : taxpayer['taxpayer_type'],
            'email'                 : taxpayer['email'],
            'birthplace'            : taxpayer['birthplace'],
            'birthdate'             : taxpayer['birthdate'],
            'bussiness'             : taxpayer['bussiness'],
            'map_area'              : {
                "province"           : taxpayer['map_area']['province'],
                "province_name"      : taxpayer['map_area']['province_name'],
                "regency"            : taxpayer['map_area']['regency'],
                "regency_name"       : taxpayer['map_area']['regency_name'],
                "district"           : taxpayer['map_area']['district'],
                "district_name"      : taxpayer['map_area']['district_name'],
                "village"            : taxpayer['map_area']['village'],
                "village_name"       : taxpayer['map_area']['village_name']
            },
            "contact"                : {
                'phone'              : taxpayer['contact']['phone'],
                'handphone'          : taxpayer['contact']['handphone'],
            },
            "address"                : {
                "street"             : taxpayer['address']['street'],
                "rt_number"          : taxpayer['address']['rt_number'],
                "rw_number"          : taxpayer['address']['rw_number'],
                "zip_code"           : taxpayer['address']['zip_code']
            },
            "occupation"                : {
                "name"                  : taxpayer['occupation']['name'],
                "working_company"       : taxpayer['occupation']['working_company'],
                "working_company_address" : taxpayer['occupation']['working_company_address']
            },
            "record_by"              : {
                "nip"                : str(employeeRecord['nip']),
                "name"               : employeeRecord['name'],
            },
            "verification_by"                : {
                "nip"                : str(employeeVerification['nip']),
                "name"               : employeeVerification['name'],
            },
            "date_record"              : taxpayer["date_record"],
            "date_verification"        : taxpayer["date_verification"]
        }

        response = helper.response_msg(
            "GET TAXPAYER SUCCESS",
            "", {},
            200
        )

        response.put('data', data)

        return response
    # end def

    # def store
    # Store a newly created resource in storage.
    def store(self, params):
        from pytavia_core import helper
        
        data = request.get_json()

        validation = taxpayer_registration.validate_payload(payload = data)

        if validation == "pass":
        
            nipEmployeeRecord       = data["record_by"]
            nipEmployeeVerification = data["verification_by"]
            villageCode             = str(data['map_area'])

            #try
            try:
                map_area_information = self.mgdDB.map_village.find_one({
                    "code" : villageCode
                })

                employeeRecord       = self.mgdDB.employee.find_one({ "nip" : nipEmployeeRecord})
                employeeVerification = self.mgdDB.employee.find_one({ "nip" : nipEmployeeVerification })

                registration_number       = self.mgdDB.taxpayer_registration.find({}).count()

                name                     = data["name"]
                register_transaction     = data["register_transaction"]
                identity_number          = data["identity_number"]
                taxpayer_type            = data["taxpayer_type"]
                email                    = data["email"]
                birthplace               = data["birthplace"]
                birthdate                = data["birthdate"]
                map_area = {
                    "province"           : map_area_information['province']['code'],
                    "province_name"      : map_area_information['province']['name'],
                    "regency"            : map_area_information['regency']['code'],
                    "regency_name"       : map_area_information['regency']['name'],
                    "district"           : map_area_information['district']['code'],
                    "district_name"      : map_area_information['district']['name'],
                    "village"            : map_area_information['code'],
                    "village_name"       : map_area_information['name']
                }
                contact                  = {
                    "phone"              : data['phone'],
                    "handphone"          : data['handphone'],
                }
                address                  = {
                    "street"             : data['address'],
                    "rt_number"          : data['rt_number'],
                    "rw_number"          : data['rw_number'],
                    "zip_code"           : data['zip_code']
                }
                occupation               = {
                    "name"               : data['occupation'],
                    "working_company"    : data['working_company'],
                    "working_company_address" : data['working_company_address']
                }
                record_by                = {
                    "pkey"               : str(employeeRecord['_id']),
                    "name"               : employeeRecord['name'],
                }
                verification_by                = {
                    "pkey"               : str(employeeVerification['_id']),
                    "name"               : employeeVerification['name'],
                }
                date_record              = data["date_record"]
                date_verification        = data["date_verification"]

                mdl_add_new_taxpayer = database.new(
                    self.mgdDB , "taxpayer_registration"
                )

                mdl_add_new_taxpayer.put("registration_number", '%010d' % (registration_number+1))
                mdl_add_new_taxpayer.put("status", "Draft")
                mdl_add_new_taxpayer.put("name", name)
                mdl_add_new_taxpayer.put("register_transaction", register_transaction)
                mdl_add_new_taxpayer.put("identity_number", identity_number)
                mdl_add_new_taxpayer.put("taxpayer_type", taxpayer_type)
                mdl_add_new_taxpayer.put("email", email)
                mdl_add_new_taxpayer.put("birthdate", birthdate)
                mdl_add_new_taxpayer.put("birthplace", birthplace)
                mdl_add_new_taxpayer.put("map_area", map_area)
                mdl_add_new_taxpayer.put("contact", contact)
                mdl_add_new_taxpayer.put("address", address)
                mdl_add_new_taxpayer.put("occupation", occupation)
                mdl_add_new_taxpayer.put("fk_record_by", record_by)
                mdl_add_new_taxpayer.put("fk_verification_by", verification_by)
                mdl_add_new_taxpayer.put("date_record", date_record)
                mdl_add_new_taxpayer.put("date_verification", date_verification)

                db_handle  = database.get_database( config.mainDB )
                bulk_multi = bulk_db_multi.bulk_db_multi({
                    "db_handle" : db_handle,
                    "app"       : self.webapp
                })
                
                bulk_multi.add_action(
                    bulk_db_multi.ACTION_INSERT ,
                    mdl_add_new_taxpayer
                )

                bulk_multi.execute({})

                return helper.response_msg("PROCESS_SUCCESS", "Taxpayer success added", { "data" : data }, 200)
                pass
            except:
                self.webapp.logger.debug( "exception occured ..." )
            # end try
        else:
            return helper.response_msg("PROCESS_FAILED", "Entity Error", { "errors" : validation }, 422)
    # end def

    # def
    # Update the specified resource in storage.
    def update(self, param):
        from pytavia_core import helper
        from bson.objectid import ObjectId

        data = request.get_json()
        pkey = data['pkey']

        response = helper.response_msg(
            "UPDATE TAXPAYER SUCCESS",
            "", {},
            200
        )

        del data["pkey"]

        validation = taxpayer_registration.validate_payload(payload = data)

        if validation == "pass":
            try:
                nipEmployeeRecord       = data["record_by"]
                nipEmployeeVerification = data["verification_by"]
                villageCode             = str(data['map_area'])

                map_area_information = self.mgdDB.map_village.find_one({
                    "code" : villageCode
                })

                employeeRecord       = self.mgdDB.employee.find_one({ "nip" : nipEmployeeRecord})
                employeeVerification = self.mgdDB.employee.find_one({ "nip" : nipEmployeeVerification })

                self.mgdDB.taxpayer_registration.update_one(
                    { "pkey" : pkey },
                    {
                        "$set" : {
                            "name"                     : data['name'],
                            "identity_number"          : data["identity_number"],
                            "taxpayer_type"            : data["taxpayer_type"],
                            "email"                    : data["email"],
                            "birthplace"               : data["birthplace"],
                            "birthdate"                : data["birthdate"],
                            "map_area"                   : {
                                    "province"           : map_area_information['province']['code'],
                                    "province_name"      : map_area_information['province']['name'],
                                    "regency"            : map_area_information['regency']['code'],
                                    "regency_name"       : map_area_information['regency']['name'],
                                    "district"           : map_area_information['district']['code'],
                                    "district_name"      : map_area_information['district']['name'],
                                    "village"            : map_area_information['code'],
                                    "village_name"       : map_area_information['name']
                            },
                            "contact"                  : {
                                "phone"              : data['phone'],
                                "handphone"          : data['handphone'],
                            },
                            "address"                : {
                                "street"             : data['address'],
                                "rt_number"          : data['rt_number'],
                                "rw_number"          : data['rw_number'],
                                "zip_code"           : data['zip_code']
                            },
                            "occupation"             : {
                                "name"               : data['occupation'],
                                "working_company"    : data['working_company'],
                                "working_company_address" : data['working_company_address']
                            },
                            "record_by"              : {
                                "pkey"               : str(employeeRecord['_id']),
                                "name"               : employeeRecord['name'],
                            },
                            "verification_by"        : {
                                "pkey"               : str(employeeVerification['_id']),
                                "name"               : employeeVerification['name'],
                            },
                            "date_record"            : data["date_record"],
                            "date_verification"      : data["date_verification"]
                        }
                    }
                )

                response.put("data", data)
                return response
                pass
            except:
                self.webapp.logger.debug( "exception occured ..." )
        else:
            return helper.response_msg("PROCESS_FAILED", "Entity Error", { "errors" : validation }, 422)
    # end def

    #def 
    # Deleted the specified resource.
    def destroy(self, param, registration_id):
        from pytavia_core import helper
        from pytavia_stdlib import utils

        response = helper.response_msg(
            "DELETE TAXPAYER SUCCESS",
            "", {},
            200
        )

        timestamp, timestamp_str    = utils._get_current_timestamp()

        self.mgdDB.taxpayer_registration.update_one(
            { "pkey" : registration_id },
            {
                "$set" : {
                    "archived_timestamp" : timestamp,
                    "archived_timestamp_str" : timestamp_str
                }
            }
        )

        response.put('data', "DELETE")

        return response
    # end def

    # def
    # validation payload
    def validate_payload(payload : dict):
        from cerberus          import Validator
        from datetime import datetime
        
        date = lambda s: datetime.strptime(s, '%Y-%m-%d')

        schema = {
            "register_transaction" : {
                "type"  : "string",
                "minlength" : 5,
                "maxlength" : 20,
                "required": True
            },
            "taxpayer_type" : {
                "type"  : "string",
                "minlength" : 3,
                "maxlength" : 20,
                "required": True
            },
            "name" : {
                "type"  : "string",
                "minlength" : 3,
                "maxlength" : 200,
                "required": True
            },
            "identity_number" : {
                "type"  : "string",
                "minlength" : 16,
                "maxlength" : 16,
                "required": True
            },
            "email" : {
                "type"  : "string",
                "maxlength" : 200,
                "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
            },
            "birthplace": {
                "type"  : "string",
                "minlength" : 3,
                "maxlength" : 255,
                "required": True
            },
            "birthdate": {
                "type"  : "date",
                'coerce': date,
                "required": True
            },
            "phone": {
                "type": "string",
                "minlength" : 8,
                "maxlength" : 13
            },
            "handphone": {
                "type": "string",
                "minlength" : 10,
                "maxlength" : 13
            },
            "address" : {
                "type": "string",
                "required"  : True,
                "minlength" : 5,
                "maxlength" : 255
            },
            "rt_number": {
                "type": "string",
                "minlength" : 3,
                "maxlength" : 3
            },
            "rw_number": {
                "type": "string",
                "minlength" : 3,
                "maxlength" : 3
            },
            "zip_code": {
                "type": "string",
                "minlength" : 5,
                "maxlength" : 5
            },
            "map_area" : {
                "type": "string",
                "minlength" : 10,
                "maxlength": 10,
                "required"  : True
            },
            "occupation": {
                "type": "string",
                "minlength" : 3,
                "maxlength" : 80,
                "required"  : True
            },
            "working_company": {
                "type": "string",
                "minlength" : 3,
                "maxlength" : 100
            },
            "working_company_address": {
                "type": "string",
                "minlength" : 3,
                "maxlength" : 255
            },
            "verification_by" : {
                "type": "string",
                "minlength" : 3,
                "maxlength" : 50,
                "required" : True
            },
            "record_by" : {
                "type": "string",
                "minlength" : 3,
                "maxlength" : 50,
                "required" : True
            },
            "date_record": {
                "type"  : 'date',
                'coerce': date,
                "required" : True
            },
            "date_verification": {
                "type"  : 'date',
                'coerce': date,
                "required" : True
            }
        }

        validator = Validator()
        validator.validate(payload, schema)

        if validator.errors:
            return validator.errors
        else:
            return "pass"
    # end def

# end class
