######################################
# author ben lawson <balawson@bu.edu>
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

from ast import Not
from contextlib import suppress
from email import message
from zmq import NULL
import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login

#for image uploading
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2867713'
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


# connects SQL database to code 
conn = mysql.connect()
cursor = conn.cursor()
# SQL query
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

# function that returns all user emails
def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()


class User(flask_login.UserMixin):
	pass

# function to access pre-existing user by email
@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user


# function that checks upon login that user exists and password matches
@login_manager.request_loader
def request_loader(request):
	# all user emails from function above
	users = getUserList()
	# email entered on website
	email = request.form.get('email')
	# deny login because value entered not compatible
	if not(email) or email not in str(users):
		return
	# creating new user object
	user = User()
	user.id = email
	# connecting to SQL
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	# accessing password from query
	pwd = str(data[0][0])
	# built-in functionality of User() class
	user.is_authenticated = request.form['password'] == pwd
	return user

'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='login' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='password' id='password' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form></br>
		   <a href='/'>Home</a>
			   '''
	#The request method is POST (page is receiving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0])
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"

@app.route('/logout')
def logout():
	flask_login.logout_user()
	# potentially want to change logout page to be different than hello page
	###############
	return render_template('logout.html', message='Logged out')

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html')

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', suppress='True')

@app.route("/register", methods=['POST'])
def register_user():
	try:
		email = request.form.get('email')
		password = request.form.get('password')
		# adding rest of attributes
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		hometown = request.form.get('hometown')
		gender = request.form.get('gender')
		birthdate = request.form.get('dob')
	except:
		print("couldn't find all tokens") #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		# SQL query to add into database
		print(cursor.execute("INSERT INTO Users (email, password, fname, lname, hometown, gender, dob) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')". \
			format(email, password, fname, lname, hometown, gender, birthdate)))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('hello.html', name=fname, message='Account Created!', suppress='True')
	else:
		print("couldn't find all tokens")
		return flask.redirect(flask.url_for('account_exists', message='This email already has an account.'))
    
# helping to display message that account exists
@app.route('/account_exists')
def account_exists():
	return render_template('register.html')

		
# function to get User photos
def getUsersPhotos(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id, caption FROM Pictures WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall() #NOTE return a list of tuples, [(imgdata, pid, caption), ...]

# function to get User friends
def getUserFriends(email):
	cursor = conn.cursor()
	cursor.execute("SELECT friend_email FROM Friends WHERE email = '{0}'".format(email))
	return cursor.fetchall()

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def getUserNameFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT fname FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def getAlbumIDFromUserAndName(user, album):
	cursor = conn.cursor()
	cursor.execute("SELECT album_id FROM Albums WHERE user_id = '{0}' and album_name = '{1}'".format(user, album))
	return cursor.fetchone()[0]

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email FROM Users WHERE email = '{0}'".format(email)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True
#end login code



@app.route('/profile')
@flask_login.login_required
def protected():
	# change display name to real name
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('hello.html', not_logged_out = True, name = getUserNameFromEmail(flask_login.current_user.id), photos=getUsersPhotos(uid), base64=base64, message="Here's your profile", heading='Here are your uploads')

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# checking if album exists
def isAlbumUnique(album, id):
#use this to check if an album has already been made by user 
	cursor = conn.cursor()
	if cursor.execute("SELECT user_id, album_name FROM Albums WHERE user_id = '{1}' and album_name = '{0}'".format(album, id)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True

def allAlbums():
	cursor = conn.cursor()
	cursor.execute("SELECT album_name, fname, lname FROM Albums, Users WHERE Albums.user_id = Users.user_id")
	all_albums = cursor.fetchall()
	return all_albums

@app.route("/viewAlbums", methods=['GET'])
def viewAlbums():
	return render_template('viewAlbums.html', message='Here are all the albums', all_albums = allAlbums())

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		caption = request.form.get('caption')
		album = request.form.get('album')
		album_date = request.form.get('album_date')
		#dont need this anymore becasue we changed primary keys
		# albumID = getAlbumIDFromUserAndName(uid, album)
		photo_data =imgfile.read()
		cursor = conn.cursor()
		#adding tags
		# tags = request.form.get('tags')

		if isAlbumUnique(album, uid):
			cursor.execute('''INSERT INTO Albums (album_name, user_id, date_ofc) VALUES (%s, %s, %s)''', (album, uid, album_date))
		conn.commit() 
		cursor.execute('''INSERT INTO Pictures (album_name, imgdata, caption, user_id) VALUES (%s, %s, %s, %s)''', (album, photo_data, caption, uid ))
		conn.commit()
		return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!', not_logged_out = True, photos=getUsersPhotos(uid), base64=base64, heading='Here are your photos')
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		return render_template('upload.html')
#end photo uploading code

	return render_template('hello.html', message='Ranked user activites on the platform')

@app.route("/albumPics", methods=['GET'])
def pics_peralbum():
	cursor = conn.cursor()
	album = 0 # CHANGE THIS TO passed album from html
	# print(album)
	cursor.execute("SELECT P.imgdata, P.picture_id, P.caption FROM Pictures as P, Albums as A WHERE P.album_name = A.album_name AND A.album_name = '{0}'".format(album))
	all_photos = cursor.fetchall()
	return render_template('hello.html', message='Photos in the album', photos=all_photos, base64=base64) 

#default page
@app.route("/", methods=['GET'])
def hello():
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id, caption FROM Pictures")
	all_photos = cursor.fetchall()
	if (all_photos):
		return render_template('hello.html', message='Welecome to Photoshares home page', photos=all_photos, base64=base64, heading='The feed')
	return render_template('hello.html', message='Welecome to Photoshares homepage')

# friends page to search and add friends
@app.route("/friends", methods=['GET'])
def friends():
	user_email = flask_login.current_user.id
	allFriends = getUserFriends(user_email)
	return render_template('friends.html', suppress='True', all_friends=allFriends)

# helping to display message that friend does not exist
@app.route('/friend_dne')
def friend_dne():
	return render_template('friends.html', message='This friend does not exist')

def are_friends(friend_email):
	cursor = conn.cursor()
	all_users = cursor.execute("SELECT email From Users")
	# all_users = cursor.fetchall()
	for user in all_users:
		cursor = conn.cursor()
		all_friends = cursor.execute("SELECT friend_email From Friends WHERE email = '{0}".format(user))
		# all_friends = cursor.fetchall()
		for friend in all_friends: 
			if friend == friend_email:
				return True
	return False

def getAllUserAct():
	cursor = conn.cursor()
	# add comments to the calculations
	cursor.execute("WITH CTE AS (SELECT U.fname, U.lname, P.user_id, count(P.picture_id) as pic_count FROM Pictures as P, Users as U WHERE P.user_id = U.user_id GROUP BY 1,2,3) SELECT fname, lname, pic_count FROM CTE ORDER BY pic_count DESC LIMIT 10")
	top_users = cursor.fetchall()
	return top_users

@app.route("/useractivity", methods=['GET'])
def activity_page():
	return render_template('userActivity.html', message='TOP 10 users with the most activity, (first name, last name, number of contributions)', TopUsers = getAllUserAct())

# helping to display message that friend does not exist
@app.route('/are_friended')
def are_friended():
	return render_template('friends.html', message='Already friends with them')

# method to add friends 
@app.route("/friends", methods=['POST'])
def add_friend():
	try:
		friend_email = request.form.get('friend_email')
	except:
		print("Couldn't find email") #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('friends'))
	cursor = conn.cursor()
	user_email = flask_login.current_user.id
	test = isEmailUnique(friend_email)
	if test==False:
		# check if the friend is already added
		if are_friends(friend_email):
			print("Already friends with them")
			return flask.redirect(flask.url_for('are_friended'))
		# SQL query to add into database
		print(cursor.execute("INSERT INTO Friends (friend_email, email) VALUES ('{0}', '{1}')".format(friend_email, flask_login.current_user.id)))
		print(cursor.execute("INSERT INTO Friends (email, friend_email) VALUES ('{0}', '{1}')".format(friend_email, flask_login.current_user.id)))
		allFriends = getUserFriends(user_email)
		conn.commit()
		return render_template('friends.html', message='Friend added!', all_friends = allFriends)
	else:
		print("Couldn't add friend")
		return flask.redirect(flask.url_for('friend_dne'))


if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=5000, debug=True)
