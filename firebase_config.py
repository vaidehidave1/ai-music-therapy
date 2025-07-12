import pyrebase

firebase_config = {
    "apiKey": "AIzaSyB4zRcNdEO_fj06foHZksZd0IBYSiHJfrI",
    "authDomain": "musicalsaathi.firebaseapp.com",
    "databaseURL": "https://musicalsaathi.firebaseio.com",
    "projectId": "musicalsaathi",
    "storageBucket": "musicalsaathi.appspot.com",
    "messagingSenderId": "86871884077",
    "appId": "1:86871884077:web:your-app-id",  # Replace with actual appId from Firebase
    "measurementId": "G-XXXXXXXXXX"             # Optional, only if you use Analytics
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()