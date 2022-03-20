from flask import Flask, redirect, url_for, render_template, request, flash
from firebase_admin import credentials, auth, firestore
import qrcode
import json

BASE_URL = 'http://127.0.0.1:5000'

# Connect to Firebase
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

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
def index():
    return render_template('index.html')


# @app.route('/signup')
# def signup():
#     return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/portal/<username>', methods = ["POST", "GET"])
def portal(username):
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            return render_template('medical_portal.html')
        except:
            return redirect('/login')
    else:
        if person["is_logged_in"] == True:
            return render_template('medical_portal.html')
        else:
            return redirect('/login')

    return render_template('medical_portal.html')

@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            # EDIT
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            return redirect(url_for('medical_portal'))
        except:
            return render_template('register.html')


def getQRCode(username):
    img = qrcode.make(f'{link}/portal/username')
    type(img)
    return img

# @app.route('/medicalInfo', methods = ["POST", "GET"])
# def medicalInfo():




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