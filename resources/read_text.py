from utils.get_api import set_image_list
from flask_restful import Resource, reqparse
from flask import jsonify
from utils.img_convert import get_image_fromb64
import cv2
from utils.storage_code import put_in_bucket, clear_bucket_images
from utils.output_notify import upload_notify
from utils.ocr_query import get_text_from_image


def upload_img(img, name):
    im_bytes = cv2.imencode(".jpg", img)[1].tobytes() #save to bucket
    put_in_bucket(name+'.jpg', im_bytes)
    
def save_json(content, filename = "json_output.json"):
    with open(filename, 'w') as mreq:
        import json
        mreq.write(json.dumps(content))

def img_resize(img):
    h, w = img.shape[:2]
    #img = cv2.resize(img, (int(w/1.2), int(h/1.2)), interpolation = cv2.INTER_AREA)
    img = cv2.resize(img, (1200, 900), interpolation = cv2.INTER_LINEAR)
    return img


class ReadText(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, required = True ,help="please enter uid") #uid can be the token or user id
        parser.add_argument('img1', type=str, required = False ,help="please enter img1")
        parser.add_argument('img2', type=str, required = False ,help="please enter img2")
        parser.add_argument('img3', type=str, required = False ,help="please enter img3")
        parser.add_argument('img4', type=str, required = False ,help="please enter img4")
        data = parser.parse_args()
        
        img1 = data["img1"]; img2 = data["img2"]; img3 = data["img3"]; img4 = data["img4"]
        if (img1 == img2 == img3 == img4 == None):
            return {"message" : "please send atleast one image"}, 400

        uid = data.pop("uid"); 
        images_list = [] #create a list of images sent to the API
        for key in data:
            if(data[key]):
                images_list.append(key)
        images_list.sort()
        print(images_list)
        
        outputs = {}
        output_images = []
        for img_name in images_list:
            img, results = get_text_from_image(base64_img=data[img_name])
            outputs[img_name] = results
            output_images.append(img)

        clear_bucket_images()

        for i in range(len(images_list)):
            img = output_images[i]
            img = img_resize(img) 
            upload_img(img, name=images_list[i])
        
        set_image_list(images=images_list)
        upload_notify(uid, "ocr", outputs)
        
        return jsonify(outputs)