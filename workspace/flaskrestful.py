from flask import Flask, g, jsonify
from flask_restful import reqparse, abort, Api, Resource
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
                          
import uuid
import os
import time
import datetime
import pytz
from itsdangerous import (TimedJSONWebSignatureSerializer
    as Serializer, BadSignature, SignatureExpired)      
app = Flask(__name__)


ACCOUNTS = {
    'acc1':{'username and password':['bob', 'joe', 'fkjsdkfsd']}
}

MESSAGES = {
    
    
}
MESSAGESID = {
    
}          
                          

app = Flask(__name__)
api = Api(app)


@staticmethod
def verify_auth_token(token):
    bool = False
    for i in range(0, len(ACCOUNTS)):
        if ACCOUNTS['acc%s' % (i + 1)][-1] == token:
            bool = True
            break
    return bool
    
def get_auth_token():
    return uuid.uuid4().hex
    
def generate_auth_token(id, expiration = 600):
    s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    return s.dumps({ 'id': id })
    


class sendMessage(Resource):
    def post(self):
        args = parser.parse_args()
        username=''
        messageid = ''
        if MESSAGESID:
            messageid = 'messagesid' + str(int(max(MESSAGES.keys()).lstrip('messagesid')) + 1)
        else:
            messageid = 'messagesid1'
        for i in range(0, len(ACCOUNTS)):
            if ACCOUNTS['acc%s' % (i + 1)]['username and password'][-1] == args['authtoken']:
                username=ACCOUNTS['acc%s' % (i + 1)]['username and password'][0]
                
        if username == '':
            return 'Token not found.'
        else:
            utc_now = pytz.utc.localize(datetime.datetime.utcnow())
            pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
            string = pst_now.isoformat()
            string = string.replace('T', ' ')
            string = string.split('.')[0]
            MESSAGESID[messageid] = {'time and message':[string] + [args['message']]}
            MESSAGES[messageid] = {'sender and sent to':[username] + args['name']}
        return MESSAGES
        
class myMessages(Resource):
    def get(self):
        args = parser.parse_args() 
        username = ''
        messagesidArr = []
        string = ''
        for i in range(0, len(ACCOUNTS)):
            if ACCOUNTS['acc%s' % (i + 1)]['username and password'][-1] == args['authtoken']:
                username=ACCOUNTS['acc%s' % (i + 1)]['username and password'][0]
                break
        if username == '':
            return "Token not found"
        else:
            for i in range(0, len(MESSAGES)):
                for c in range(1, len(MESSAGES['messagesid%s' % (i + 1)]["sender and sent to"])):
                    if MESSAGES['messagesid%s' % (i + 1)]["sender and sent to"][c] == username:
                        string += 'Date: ' + MESSAGESID['messagesid%s' % (i + 1)]['time and message'][0] + ' Sender: ' + MESSAGES['messagesid%s' % (i + 1)]['sender and sent to'][0] + ' Message: ' + MESSAGESID['messagesid%s' % (i + 1)]['time and message'][1]
                        string += '\n '
            string += 'end'
            return string
            
api.add_resource(myMessages, "/viewmessages")
api.add_resource(sendMessage, '/sendmessage')


def abort_if_todo_doesnt_exist(account):
    if account not in ACCOUNTS:
        abort(404, message="Todo {} doesn't exist".format(account))

parser = reqparse.RequestParser()
parser.add_argument('name', action='append')
parser.add_argument('authtoken')
parser.add_argument('message')
parser.add_argument('password')


class manageaccounts(Resource):
    def get(self):
        return ACCOUNTS

    def post(self):
        args = parser.parse_args()
        str = get_auth_token()
        arr = args['name'] + [args['password']] + [str]
        account = int(max(ACCOUNTS.keys()).lstrip('acc')) + 1
        account = 'acc%i' % account
        ACCOUNTS[account] = {'username and password': arr}
        return ACCOUNTS[account], 201
        
class token(Resource):
    def get(self):
        username = ''
        password = ''
        args = parser.parse_args()
        for i in range(0, len(ACCOUNTS)):
            if ACCOUNTS['acc%s' % (i + 1)]['username and password'][-1] == args['authtoken']:
                username=ACCOUNTS['acc%s' % (i + 1)]['username and password'][0]
                password=ACCOUNTS['acc%s' % (i + 1)]['username and password'][1]
                
        if username != '' and password != '':
            return 'Username: ' + str(username) + ' ' + 'Password: ' + str(password)
        else:
            return 'No token found.'
            
api.add_resource(token, '/token')
            
class login(Resource):
    def get(self):
        
        print(ACCOUNTS['acc1'])
        args = parser.parse_args()
        str = get_auth_token()
        arr = args['name']
        bool = False
        logincombo = args['name'] + [args['password']]
        for i in range(0, len(ACCOUNTS)):
            if ACCOUNTS['acc%s' % (i + 1)]['username and password'][:-1] == logincombo:
                ACCOUNTS['acc%s' % (i + 1)]['username and password'] = ACCOUNTS['acc%s' % (i + 1)]['username and password'][:2] + [str]
                return str
            
        else: 
            return 'Login not found.'
    


api.add_resource(manageaccounts, '/account')
api.add_resource(login, '/login')


if __name__ == '__main__':
    host=os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    app.debug = True
    app.secret_key = 'PBN\xbb\xae"\xe7\xc6\x98\xe2w\x0fB\xa3\x1e\xa0\x1d6(\xda:Kq\xd7'
    app.run(host=host, port=port)
    