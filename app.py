from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

#import resources
from resources.object_detect import ObjectDetect

# create flask app instance
app = Flask(__name__)

#set config for jwt
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY'] = 'qp-cbit'

#initialize api
api = Api(app)

api.add_resource(ObjectDetect, '/object-detect') #for admin to upload paper with an optional feature to set select_status=1

jwt=JWTManager(app)

#a welcome route to test if the flask app is working.
@app.route('/')
def home():
    return(f"""<h1 style="font-family: 'Palatino Linotype';">This is an API for the Smart blind assistant system.</h1>
                <p style="font-size:2em">Developed by Harish Akula</p>""")

# set debug = False while deploying. debug = True is not safe in production environments
if __name__ == '__main__':
    app.run(port=5000, debug=True)