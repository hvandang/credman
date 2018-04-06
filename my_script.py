from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import sqlite3

# create application object of class Flask
app = Flask(__name__)
api = Api(app)

# This HelloWorld method is just for testing
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
api.add_resource(HelloWorld, '/')


parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)

#The API class that handles the authentication
class Authenticate(Resource):
	def post(self):
		# parse user name, password
		args = parser.parse_args()
		un = str(args['username'])
		pw = str(args['password'])
		# verify user name, password
		return check_auth(un,pw)
		
# Verify user name, password    		
def check_auth(username, password):
    return username == 'user' and password == '123'

api.add_resource(Authenticate, '/auth')

# Add users
class AddUser(Resource):
	def __init__(self):
		# create database at initilization
		create_db()
	def post(self):
		adduser('user3','user3@mail.com','123')
		user = get_user()
		return user[0] #print the 1st column retrieved(username)

# define constants
# database name
db_credential = 'credential'
# table name
tb_user = 'users'

# Create database named credential, and table named users. Add 1 default user into database
def create_db():
	try:
		# create database 'credential' in the text file 'credential'. This file is in the current folder.
		db = sqlite3.connect(db_credential)		
		# create table 'users'
		cursor = db.cursor()	
		# create table 
		cursor.execute('''
    	CREATE TABLE %s(id INTEGER PRIMARY KEY, username TEXT unique, email TEXT unique, password TEXT)
		'''%(tb_user))		
		# commit changes
		db.commit()
	# Catch the exception
	except Exception as e:
		# Roll back any change if something goes wrong
		db.rollback()
		raise
	finally:
   		# Close the db connection
		db.close()

# Add a user to database credential		
def adduser(uname, email, password):
	try:
		# connect database
		db = sqlite3.connect(db_credential)
		cursor = db.cursor()		
		# add user
		cursor.execute('''INSERT INTO %s(username, email, password)
   	               VALUES(?,?,?)'''%(tb_user), (uname, email, password))		
		# commit changes
		db.commit()
	# Catch the exception
	except Exception as e:
		# Roll back any change if something goes wrong
		db.rollback()
		raise
	finally:
   		# Close the db connection
		db.close()

# Get a user from the database credential
def get_user():
	try:
		# connect database
		db = sqlite3.connect(db_credential)
		cursor = db.cursor()
		# query user	
		cursor.execute('''SELECT username, password FROM %s'''%(tb_user))
		#retrieve the first row
		user1 = cursor.fetchone()
		return user1
	# Catch the exception
	except Exception as e:
		# Roll back any change if something goes wrong
		db.rollback()
		raise
	finally:
   		# Close the db connection
		db.close()
		
api.add_resource(AddUser, '/adduser')
	
if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=5001)