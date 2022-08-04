import iso8583
import banksumut

class protocol8583:
    mapping_message = {
        "desc"          : "message_desc"  ,
        "provider"      : "provider"      ,
        "status_code"   : "status_code"   ,
        'iso_version'   : "iso_version"   ,
        'message_in'    : "message_in"    ,
        'message_out'   : "message_out"
    }

    def process(provider, message, encodeType = 'raw'):
        messageHeader                   = protocol8583._getHeader(message)
        messageISOVersion               = protocol8583._getISOVersion(message)
        totalHeader                     = len(messageHeader) + len(messageISOVersion)

        messageISO8583                  = message[totalHeader:len(message)]

        protocol8583.mapping_message['desc']        = 'Inquery Process'
        protocol8583.mapping_message['provider']    = provider
        protocol8583.mapping_message['message_in']  = messageISO8583.decode('utf-8')
        protocol8583.mapping_message['iso_version'] = messageISOVersion.decode('utf-8')

        if provider == 'bnksumut':
            profileProvider = banksumut.sumutSpec
        elif provider == 'bnkbri':
            profileProvider = None

        decoded, encoded = iso8583.decode(messageISO8583, profileProvider)
        
        messageISO8583 = banksumut.process(decoded, encodeType)

        if encodeType == 'raw':
            messageISO8583 = messageISOVersion.decode('utf-8') + messageISO8583
            messageISO8583 = str(len(messageISO8583)) + messageISO8583

        protocol8583.mapping_message['status_code']     = 200
        protocol8583.mapping_message['message_out']     = messageISO8583

        return protocol8583.mapping_message

    def _setMessage(message):
        return message[4:12]

    def _getHeader(message):
        return message[0:4]

    def _getISOVersion(message):
        return message[4:16]