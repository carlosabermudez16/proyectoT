import os
from dotenv import load_dotenv
from matplotlib.pyplot import get

load_dotenv()

class Config:
    host = os.getenv("HOST")
    database = os.getenv("DATABASE") 
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    firebase_connetion = {

                "apiKey": "AIzaSyCzL3UdeLClqJ5Z5TF76FIZ23UCyXtDZ28",
                "authDomain": "iasssystem.firebaseapp.com",
                "databaseURL": "https://iasssystem-default-rtdb.firebaseio.com",
                "projectId": "iasssystem",
                "storageBucket": "iasssystem.appspot.com",
                "messagingSenderId": "279204958241",
                "appId": "1:279204958241:web:f8a3c4d5d3e927b5a71360"
            }
    email = os.getenv("EMAIL")
    password_email = os.getenv("PASSWORD_EMAIL")



#debug_mode = { 'development': Config }