import firebase_admin

databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
cred_obj = firebase_admin.credentials.Certificate("fbServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL
	})

from firebase_admin import db

def get_endpoint(model_name):
    ref = db.reference("/"+model_name)
    return ref.get()