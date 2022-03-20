from flask import Flask, redirect, url_for, render_template, request, flash
# from firebase_admin import credentials, auth, firestore
import pyrebase
# import firebase_admin
import qrcode
import json

BASE_URL = 'http://127.0.0.1:5000'

# Connect to Firebase Firestore
# cred = credentials.Certificate('firebase-admin.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# Connect to Firebase Realtime Database
config = {
  "apiKey": "AIzaSyBGRn-c9Cl6kbROuWu44w5besGDNxsDM5I",
  "authDomain": "retro-c0350.firebaseapp.com",
  "projectId": "retro-c0350",
  "databaseURL": "https://retro-c0350-default-rtdb.firebaseio.com/",
  "storageBucket": "retro-c0350.appspot.com",
  "messagingSenderId": "112454151211",
  "appId": "1:112454151211:web:abd98d22947b2b37ba0e6e"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__)

# Views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["password"]
        name = result["name"]
        date_of_birth = result["date_of_birth"]
        if email is None or password is None or name is None or date_of_birth is None:
            return {'message': 'Error missing information'}, 400
        try:
            auth.create_user_with_email_and_password(email, password)
            print('success')
            user = auth.sign_in_with_email_and_password(email, password)
            print(user['localId'])
            # id = user['localId']
            url = f'{BASE_URL}/portal/{id}'
            print('url created')

            # Firebase Realtime Database
            data = {
                "id": id,
                "name": name,
                "email": email,
                "date_of_birth": date_of_birth,
                "url": url
            }
            db.child("users").child(id).set(data)
            print('database updated')


            return redirect('portal/{}'.format(user['localId']))
        except:
            print('error creating user')
            return {'message': 'Error creating user'}, 400
    else:
        return render_template('signup.html')


@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["password"]
        if email is None or password is None:
            return {'message': 'Error missing information'}, 400
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(user['localId'])

            return redirect(url_for('portal/{}'.format(user['localId'])))
        except:
            return {'message': 'Error logging in'}, 400
    else:
        return render_template('login.html')


@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/portal/<id>')
def portal(id):
    db = firebase.database()
    user = db.child("users").child(id).get()

    # users = db.child("users").get()



    return render_template('medical_portal.html')


def getQRCode(id):
    img = qrcode.make('{}/portal/{}}'.format(BASE_URL, id))
    type(img)
    return img

if __name__ == '__main__':
    app.run(debug=True)