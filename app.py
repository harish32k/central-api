from flask import Flask, jsonify
from flask_restful import Api

# create flask app instance
app = Flask(__name__)

#set config
app.config['PROPAGATE_EXCEPTIONS']=True

#initialize api
api = Api(app)

#import resources
from resources.object_detect import ObjectDetect
from resources.depth_estimate import DepthEstimate
from resources.read_text import ReadText
from resources.captioning import Captioning
#from resources.new_captioning import NewCaption as Caption
from resources.grief_signaling import GriefSignaling
from resources.object_and_depth import ComputeObjectDepth

api.add_resource(ObjectDetect, '/object-detect')
api.add_resource(DepthEstimate, '/depth-estimate')
api.add_resource(ReadText, '/read-text')
api.add_resource(Captioning, '/captioning')
api.add_resource(GriefSignaling,'/grief-signaling')
api.add_resource(ComputeObjectDepth,'/object-and-depth')


import firebase_admin
import os
databaseURL = "https://api-endpoints-3d693-default-rtdb.firebaseio.com"
cred_obj = firebase_admin.credentials.Certificate(os.path.join('tokens', 'fbServiceAccountKey.json'))
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL,
    'storageBucket': 'api-endpoints-3d693.appspot.com'
	})

#a welcome route to test if the flask app is working.
@app.route('/')
def home():
    return(f"""<h1 style="font-family: 'Palatino Linotype';">This is an API for the Smart blind assistant system.</h1>
                <p style="font-size:2em">Developed by Harish Akula</p>""")

@app.route('/tester')
def my_checker():
    return jsonify({"message" : "hello, this app is successfully working"})

# set debug = False while deploying. debug = True is not safe in production environments
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)