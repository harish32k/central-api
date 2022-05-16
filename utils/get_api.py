import firebase_admin
import os
"""
databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
cred_obj = firebase_admin.credentials.Certificate(os.path.join('tokens', 'fbServiceAccountKey.json'))
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL,
    'storageBucket': 'api-endpoints-3d693.appspot.com'
	})"""

from firebase_admin import db

def get_endpoint(model_name):
    ref = db.reference("/deployment/"+model_name)
    return ref.get()

def get_image_list():
    ref = db.reference("/recent/img_list/")
    return ref.get()

def set_image_list(images):
    ref = db.reference("/recent/img_list/")
    return ref.set(images)



if __name__ == '__main__':
    import os
    databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
    cred_obj = firebase_admin.credentials.Certificate(os.path.join('tokens', 'fbServiceAccountKey.json'))
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':databaseURL,
        'storageBucket': 'api-endpoints-3d693.appspot.com'
        })