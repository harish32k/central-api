from get_api import get_endpoint
from flask_restful import Resource, reqparse
from flask import jsonify

# this resource is for the users to get papers for a subject yearwise
class ObjectDetect(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('img1', type=str, required = False ,help="please enter img1")
        parser.add_argument('img2', type=str, required = False ,help="please enter img2")
        parser.add_argument('img3', type=str, required = False ,help="please enter img3")
        parser.add_argument('img4', type=str, required = False ,help="please enter img4")
        data = parser.parse_args()
        
        img1 = data["img1"]
        img2 = data["img2"]
        img3 = data["img3"]
        img4 = data["img4"]
        
        
        if (img1 == img2 == img3 == img4 == None):
            return {
                "message" : "please send atleast one image"
            }, 400

        
        
        return jsonify(get_endpoint('object'))
