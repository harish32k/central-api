import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from utils.get_api import get_image_list, set_image_list
import os


"""
cred = credentials.Certificate("fbServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'api-endpoints-3d693.appspot.com'
})"""

def get_bucket():
    bucket = storage.bucket()
    return bucket

def put_in_bucket(blob_name, contents):
    bucket = get_bucket()
    blob = bucket.blob(blob_name)
    blob.upload_from_string(contents, content_type="image/jpeg")

def clear_bucket_images():
    image_list = get_image_list()
    if image_list == None:
        return
    set_image_list([])
    bucket = get_bucket()
    for image in image_list:
        blob = bucket.blob(image+'.jpg')
        blob.delete()
    

# 'bucket' is an object defined in the google-cloud-storage Python library.
# See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
# for more details.


"""
blob = bucket.blob(destination_blob_name)

blob.upload_from_string(contents)
"""

if __name__ == '__main__':
    import os
    databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
    cred_obj = firebase_admin.credentials.Certificate(os.path.join('tokens', 'api-endpoints-3d693-firebase-adminsdk-riezz-1e41a2e841.json'))
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':databaseURL,
        'storageBucket': 'api-endpoints-3d693.appspot.com'
        })
    bucket = get_bucket("object")
    blob = bucket.blob("newfile.txt")
    blob.upload_from_string("hello_world.txt")