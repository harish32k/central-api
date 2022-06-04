from utils.get_api import get_endpoint, set_image_list
from flask_restful import Resource, reqparse
from flask import jsonify, request
from utils.storage_code import put_in_bucket, clear_bucket_images
from utils.output_notify import upload_notify


class FaceDetect(Resource):

    def post(self):
        data = request.get_json(force=True)

        print(data)
        '''parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, required = True ,help="please enter uid") #uid can be the token or user id
        parser.add_argument('front', type=str, required = False ,help="please enter front")
        parser.add_argument('right', type=list, required = False ,help="please enter right")
        parser.add_argument('back', type=list, required = False ,help="please enter back")
        parser.add_argument('left', type=list, required = False ,help="please enter left")
        data = parser.parse_args()'''
        
        '''img1 = data["front"]; img2 = data["right"]; img3 = data["back"]; img4 = data["left"]
        if (img1 == img2 == img3 == img4 == None):
            return {"message" : "please send atleast one image"}, 400'''

        uid = data.pop("uid"); 
        outputs = data
        clear_bucket_images()

        set_image_list(images=[])
        upload_notify(uid, "face", outputs)
        
        return jsonify(data) #{"message" : "success"}