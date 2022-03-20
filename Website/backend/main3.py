from flask import Flask, redirect, url_for, render_template, request, flash
from firebase_admin import credentials, auth
import qrcode
import firebase_admin
import json
import pyrebase


# Connect to firebase
# cred = credentials.Certificate("firebase-admin.json")
# firebase_admin.initialize_app(cred)
# pb = pyrebase.initialize_app(json.load(open('firebase-config.json')))

#initialize firebase
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# db = firebase.database()

#Initialze person as dictionary
# person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

app = Flask(__name__)

# Authentication
# def check_token(f):
#     @wraps(f)
#     def wrap(*args,**kwargs):
#         if not request.headers.get('authorization'):
#             return {'message': 'No token provided'},400
#         try:
#             user = auth.verify_id_token(request.headers['authorization'])
#             request.user = user
#         except:
#             return {'message':'Invalid token provided.'},400
#         return f(*args, **kwargs)
#     return wrap


# @app.route('/api/userinfo')
# @check_token
# def userinfo():
#     return {'data': users}, 200


# Views
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')
@app.route('/portal/<username>')
def portal(username):
    # return f'User {escape(username)}'
    return render_template('medical_portal.html')


# API
# @app.route('/api/signup')
# def signup():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if email is None or password is None:
#         return {'message': 'Error missing email or password'},400
#     try:
#         user = auth.create_user(
#                email=email,
#                password=password
#         )

            
        
#         return {'message': f'Successfully created user {user.uid}'},200
#     except:
#         return {'message': 'Error creating user'},400

# @app.route('/api/token')
# def token():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     try:
#         user = pb.auth().sign_in_with_email_and_password(email, password)
#         jwt = user['idToken']
#         return {'token': jwt}, 200
#     except:
#         return {'message': 'There was an error logging in'},400

if __name__ == '__main__':
    app.run(debug=True)