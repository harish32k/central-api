import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import utils.fcm_manager as fcm

def upload_json(task, prediction):
    ref = db.reference("/recent")
    task_ref = ref.child("task")
    task_ref.set(task)
    pred = ref.child("prediction")
    pred.set(prediction)


def upload_notify(uid, task, prediction):
    upload_json(task, prediction)
    fcm.send_push("Success", task, [uid])


if __name__ == '__main__':
    import os
    databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
    cred_obj = firebase_admin.credentials.Certificate(os.path.join('tokens', 'fbServiceAccountKey.json'))
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':databaseURL,
        'storageBucket': 'api-endpoints-3d693.appspot.com'
        })