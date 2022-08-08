import pprint
from pytavia_core      import database
from pytavia_core      import config

from flask             import jsonify, request

# adding comments

class transactionIso8583:

    mgdDB = database.get_db_conn(config.mainDB)

    # def
    def __init__(self, app):
        self.webapp = app
    # end def

    def encodedMessage(self, param):
        import iso8583
        
        from pytavia_core   import helper
        from pytavia_stdlib.specISO8583 import banksumut


        data = request.get_json()

        profileProvider = banksumut.sumutSpec

        message = {
            't'         : str(data['mti']),
            '2'         : str(data['pan']),
            '3'         : str(data['processing_code']),
            '4'         : str(data['amount_transaction']),
            '7'         : str(data['transmission_datetime']),
            '11'        : str(data['system_trace_audit_number']),
            '12'        : str(data['time_local_transaction']),
            '13'        : str(data['date_local_transaction']),
            '18'        : str(data['merchant_type']),
            '32'        : str(data['acquiring_institution']),
            '37'        : str(data['retrieval_reference_number']),
            '41'        : str(data['card_acceptor']),
            '48'        : str(data['additional_number'].ljust(21, ' ')),
            '49'        : str(data['transaction_code'])
        }

        decoded, encoded = iso8583.encode(message, profileProvider)

        response = helper.response_msg(
            "ENCODED MESSAGE PROCESS",
            "", {},
            200
        )

        messageISO8583 = 'ISO005000017' + decoded.decode('utf-8')

        data = {
            'hex'       : encoded['p']['data'].decode('utf-8'),
            'raw'       : str(len(messageISO8583)).rjust(4, '0') + messageISO8583
        }

        response.put('data', data)

        return response


    def decodedMessage(self, param):
        from pytavia_core   import helper
        from pytavia_stdlib.specISO8583 import banksumut
        from pytavia_stdlib import protocol8583

        response = helper.response_msg(
            "DECODED MESSAGE PROCESS",
            "", {},
            200
        )


        data = request.get_json()

        incomingMessage = data['message']

        provider = 'bnksumut'

        message = protocol8583.protocol8583.process(provider, incomingMessage.encode('utf-8'), encodeType="raw")

        response.put('data', message)

        return response