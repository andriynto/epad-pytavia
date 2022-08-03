import bcrypt

from collections       import namedtuple
from flask             import jsonify, request, session

from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import bulk_db_multi

# adding comments

class authenticaton:

    mgdDB = database.get_db_conn(config.mainDB)

    # def
    def __init__(self, app):
        self.webapp = app
    # end def

    def signin(self, param):
        from pytavia_core import helper

        response = helper.response_msg(
            "LOGIN PROCESS",
            "", {},
            200
        )

        req = request.get_json()

        validation = authenticaton.validation_payload_signin(payload = req)

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if validation == "pass":

            login_user = self.mgdDB.users.find_one({
                "$or"   :[{
                        "username"  : username
                    },
                    {
                        "email"     : username
                    }
                ]
            })

            if login_user:
                if bcrypt.checkpw(password.encode('utf-8'), login_user['password']):
                    session['username'] = username
                    session['role']     = login_user['role']

                    response.put('status_code', 200)
                    response.put('data', 'login success')
                else:
                    response.put('status_code', 400)
                    response.put('data', { 'errors' : { 'authentication' : 'Invalid username or email/password combination!!' }})
            else:
                response.put('status_code', 400)
                response.put('data', { 'errors' : { 'username' : 'Invalid username'}})
        else:
            response.put('data', {"errors" : validation})
            response.put('status_code', 422)

        return response

    def signup(self, param):
        from pytavia_core import helper

        response = helper.response_msg(
            "SIGNUP PROCESS",
            "", {},
            200
        )

        req = request.get_json()

        validation = authenticaton.validation_payload_signup(payload = req)

        if validation == "pass":
            if req['password'] != req['password_confirmation']:
                response.put('data', { "errors" : {
                    "password_confirmation"  : "password and password confirmation not same"
                }})

                response.put('status_code', 422)
            else:
                user       = self.mgdDB.users

                #start check existing user
                existing_user = user.find_one({
                    "$or"   :[{
                            "username"  : req['username']
                        },
                        {
                        "email" : req['email']
                    }]
                })
                
                if existing_user is None:
                    #start save new user register to database
                    hashed   = bcrypt.hashpw(request.json.get('password').encode('utf-8'), bcrypt.gensalt())

                    # response.put('data', {"errors" : hashed.decode('utf-8') })
                    # response.put('status_code', 422)
                    # return response
                    name            = req["name"]
                    username        = req["username"]
                    email           = req["email"]
                    password        = hashed
                    role            = "Pendataan"

                    mdl_add_user = database.new(
                        self.mgdDB , "users"
                    )

                    mdl_add_user.put( "name" , name)
                    mdl_add_user.put( "username" , username)
                    mdl_add_user.put( "email" , email)
                    mdl_add_user.put( "password", password )
                    mdl_add_user.put( "role" , role )

                    db_handle  = database.get_database( config.mainDB )
                    bulk_multi = bulk_db_multi.bulk_db_multi({
                        "db_handle" : db_handle,
                        "app"       : self.webapp
                    })
                    bulk_multi.add_action(
                        bulk_db_multi.ACTION_INSERT ,
                        mdl_add_user
                    )

                    bulk_multi.execute({})
                    #end save

                    #start save session
                    session['username'] = username
                    session['role'] = role
                    
                    response.put("data", 'User success created')
                    response.put('status_code', 200)
                else:
                    response.put("data", 'Username / email has exist')
                    response.put('status_code', 400)
                
        else:
            response.put('data', {"errors" : validation})
            response.put('status_code', 422)

        return response

        


        user       = self.mgdDB.users
        existing_user = user.find_one({'name' : req['username']})

    def validation_payload_signin(payload):
        from cerberus          import Validator
        
        schema = {
            "username" : {
                "type"  : "string",
                "minlength" : 5,
                "maxlength" : 100,
                "required": True
            },
            "password" : {
                "type"  : "string",
                "minlength" : 3,
                "maxlength" : 50,
                "required": True
            }
        }

        validator = Validator()
        validator.validate(payload, schema)

        if validator.errors:
            return validator.errors
        else:
            return "pass"

    def validation_payload_signup(payload):
        from cerberus          import Validator
        
        schema = {
            "name" : {
                "type"  : "string",
                "minlength" : 5,
                "maxlength" : 20,
                "required": True
            },
            "username" : {
                "type"  : "string",
                "minlength" : 5,
                "maxlength" : 50,
                "required": True
            },
            "email" : {
                "type"  : "string",
                "minlength" : 3,
                "maxlength" : 100,
                "required": True,
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            },
            "password" : {
                "type"  : "string",
                "minlength" : 3,
                "maxlength" : 100,
                "required": True
            },
            "password_confirmation" : {
                "type"  : "string",
                "minlength" : 3,
                "maxlength" : 100,
                "required": True
            }
        }

        validator = Validator()
        validator.validate(payload, schema)

        if validator.errors:
            return validator.errors
        else:
            return "pass"