#!/usr/bin/env python3
import sys
import json
import settings
import cgitb
import cgi
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
from db_util import db_access

cgitb.enable()
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'madacamiaNut'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

api = Api(app)
usr = 0

def getUserID(username):
    sqlProc = 'getUserID'
    sqlArgs = [username]
    try:
        rows = db_access(sqlProc,sqlArgs)
        x = rows[0]
        userid = x['user_id']
    except Exception as e:
        abort(500, e)
    return userid

#All curl scripts are numbered inside curl_scripts file
class Root(Resource):
	def get(self):
		return app.send_static_file('index.html')
class LogIn(Resource):

    #curl_scripts(1)
    def post(self):
        if not request.json:
            abort(400)
        parser = reqparse.RequestParser()
        try:
            parser.add_argument('username', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            request_params = parser.parse_args()
        except:
            abort(400)
        
        if request_params['username'] in session:
            response = {'status': 'Success'}
            responseCode = 200
        else:
            try:
                ldapServer = Server(host=settings.LDAP_HOST)
                ldapConnection = Connection(ldapServer,
                                raise_exceptions=True,
                                user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					            password = request_params['password'])
                ldapConnection.open()
                ldapConnection.start_tls()
                ldapConnection.bind()
                session['username'] = request_params['username']
                response = {'status': 'success' }
                responseCode = 201
                args = [session['username']]
                try:
                    if(db_access("getUserwithUsername", args) == ()):
                        db_access("addUser", args)
                except Exception as e:
                    abort(500, e)
                global usr
                usr = getUserID(session['username'])
            except (LDAPException):
                response = {'status': 'Access denied'}
                responseCode = 403
            finally:
                ldapConnection.unbind()

        return make_response(jsonify(response), responseCode)
    
    #curl_scripts(2)
    def get(self):
        if 'username' in session:
            response = {'status': 'success'}
            responseCode = 200
        else:
            response = {'status': 'fail'}
            responseCode = 403

        return make_response(jsonify(response), responseCode)
    
    #curl_scripts(3)
    def delete(self):
        if 'username' in session:
            session.pop('username',None)
            response = {'status': 'Logged Out'}
            responseCode = 200
        else:
            response = {'status': 'fail'}
            responseCode = 403

        return make_response(jsonify(response), responseCode)

class PersonalList(Resource):
    #curl_scripts(4)
    def get(self):
        sqlProc = 'showList'
        sqlArgs=[usr]
        try:
            rows = db_access(sqlProc,sqlArgs)
        except Exception as e:
            abort(500, e)
        return make_response(jsonify({'presents':rows}), 200)

class PersonalListPresent(Resource):
    #curl_scripts(5)
    def put(self, presentId):
        quantity = request.json["Quantity"]
        sqlProc = 'updateQuantity'
        sqlArgs = [presentId, quantity, usr]
        try:
            rows = db_access(sqlProc, sqlArgs)
        except Exception as e:
            abort(500, e)
        return make_response("Successfully Updated the Quantity", 200)
    
    #curl_scripts(6)
    def delete(self, presentId):
        sqlProc = 'remove_present_from_list'
        sqlArgs = [presentId,usr]
        try:
            rows = db_access(sqlProc, sqlArgs)
        except Exception as e:
            abort(500, e)
        return make_response('Successfully deleted item from list', 200)

class Presents(Resource):
    #curl_scripts(7)
    def get(self):
        sqlProc = 'getPresents'
        sqlArgs=[]
        try:
            rows = db_access(sqlProc,sqlArgs)
        except Exception as e:
            abort(500, e)
        return make_response(jsonify({'presents':rows}), 200)
    
    #curl_scripts(8)
    def post(self):

        present_name = request.json['Present_Name']
        vendor = request.json['Vendor']
        cost = request.json['Cost']

        sqlProc = 'addPresent'
        sqlArgs = [present_name,vendor,cost]

        try:
            row=db_access(sqlProc,sqlArgs)
        except Exception as e:
            abort(500,e)

        uri = request.base_url+'/'+str(row[0]['LAST_INSERT_ID()'])
        return make_response(jsonify( { "uri" : uri } ), 200)

class Present(Resource):
    #curl_scripts(9)
    def get(self,presentId):
        sqlProc = 'getPresent'
        sqlArgs = [presentId,]
        try:
            rows = db_access(sqlProc,sqlArgs)
        except Exception as e:
            abort(500, e)
        return make_response(jsonify({'present':rows}), 200)
    
    #curl_scripts(10)
    def post(self,presentId):

        quantity = request.json["Quantity"]
        sqlProc = 'addPresentToList'
        sqlArgs = [usr,presentId,quantity]
        try:
            row = db_access(sqlProc, sqlArgs)
        except Exception as e:
            abort(500, e) 

        return make_response('Successfully added', 200)
    
    #curl_scripts(11)
    def delete(self,presentId):
        sqlProc = 'delete_present'
        sqlArgs = [presentId]
        try:
            row = db_access(sqlProc, sqlArgs)
        except Exception as e:
            abort(500, e) 

        return make_response('Successfully deleted', 200)

class Users(Resource):
    #curl_scripts(12)
    def get(self):
        sqlProc = 'getUsers'
        sqlArgs=[]
        try:
            rows = db_access(sqlProc,sqlArgs)
        except Exception as e:
            abort(500, e)
        return make_response(jsonify({'User':rows}), 200)

class User(Resource):
    #curl_scripts(13)
    def get(self,userId):
        if 'username' in session:
            sqlProc = 'getUser'
            sqlArgs=[userId]
            try:
                rows = db_access(sqlProc,sqlArgs)
            except Exception as e:
                abort(500, e)
            return rows
        else:
            return 'User not in session'

class UserList(Resource):
    
    #curl_scripts(14)
    def get(self,userId):
        sqlProc = 'showList'
        sqlArgs=[userId]
        try:
            rows = db_access(sqlProc,sqlArgs)
            userInfo = User.get(self, userId)
        except Exception as e:
            abort(500, e)
        return make_response(jsonify({'User': userInfo, "present": rows}), 200)

api.add_resource(Root,'/')
api.add_resource(LogIn, '/login')
api.add_resource(PersonalList, '/myList')
api.add_resource(PersonalListPresent, '/myList/<int:presentId>')
api.add_resource(Presents,'/presents')
api.add_resource(Present,'/presents/<int:presentId>')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:userId>')
api.add_resource(UserList, '/users/<int:userId>/presents/')

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, ssl_context=context, debug=settings.APP_DEBUG)
