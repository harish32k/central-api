"""from img_convert import get_image_fromb64
import cv2
from storage_code import put_in_bucket
import firebase_admin

databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
cred_obj = firebase_admin.credentials.Certificate("fbServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL,
    'storageBucket': 'api-endpoints-3d693.appspot.com'
	})



im = "img1"
val = ""
with open("myjson.json", 'r') as j:
    val = j.read()
d = eval(val)
s = d["img1"]
img = get_image_fromb64(s)
img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
im_bytes = cv2.imencode(".jpg", img)
print(im_bytes)
put_in_bucket(im+'.jpg', im_bytes)
cv2.imwrite(im+'.jpg', img)"""


outputs = {
            "img1" :
            [{
                "class": 64,
                "confidence": 0.8905174732,
                "name": "mouse",
                "xmax": 1599.552734375,
                "xmin": 1392.1690673828,
                "ymax": 1116.3695068359,
                "ymin": 902.0318603516
            },
            {
                "class": 63,
                "confidence": 0.6385954618,
                "name": "laptop",
                "xmax": 1522.5570068359,
                "xmin": 472.3603820801,
                "ymax": 778.096862793,
                "ymin": 87.282333374
            },
            {
                "class": 66,
                "confidence": 0.4632259011,
                "name": "keyboard",
                "xmax": 1463.640625,
                "xmin": 0.0,
                "ymax": 1122.6491699219,
                "ymin": 718.2955932617
            },
            {
                "class": 66,
                "confidence": 0.2704735994,
                "name": "keyboard",
                "xmax": 1292.5861816406,
                "xmin": 694.598815918,
                "ymax": 657.5953369141,
                "ymin": 543.4806518555
            }]
        }
        

from utils.img_convert import get_image_fromb64
import cv2
from utils.storage_code import put_in_bucket
import firebase_admin
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join('tokens', 'fbServiceAccountKey.json')

databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
cred_obj = firebase_admin.credentials.Certificate("fbServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL,
    'storageBucket': 'api-endpoints-3d693.appspot.com'
	})

from google.cloud import storage

import json
from utils.storage_code import get_bucket
bucket = get_bucket()
blob = bucket.blob('output.json')
blob.upload_from_string(json.dumps(outputs), content_type='application/json')

print(json.dumps(outputs))

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )
    #blob.delete()


download_blob('api-endpoints-3d693.appspot.com', 'output.json', 'fb_output.json')