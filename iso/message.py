import os
import sys
from bson import encode
import iso8583
import sys
import pprint
import protocol8583
import iso8583
import banksumut

# Incoming message with iso8583
incomingMessage = '0151ISO00500001702007238400108818000166274860024132493360000000000000000080407172406186714172408047016040117220804061701024132490211209411011001222161  360'

provider = 'bnksumut'
message = protocol8583.protocol8583.process(provider, incomingMessage.encode('utf-8'), encodeType = 'raw')

pprint.pp(message)