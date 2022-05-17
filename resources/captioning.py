from utils.ai_platform_predict import call_model
from utils.get_api import get_endpoint, set_image_list
from flask_restful import Resource, reqparse
from flask import jsonify
from utils.img_convert import get_image_fromb64
import cv2
from utils.storage_code import put_in_bucket, clear_bucket_images
from utils.output_notify import upload_notify
import requests

def img_resize(base64_image):
    myimg = get_image_fromb64(base64_image)
    myimg = cv2.cvtColor(myimg , cv2.COLOR_BGR2RGB)
    h, w = myimg.shape[:2]
    myimg = cv2.resize(myimg, (int(w/1.2), int(h/1.2)), interpolation = cv2.INTER_AREA)
    return myimg

def get_caption(base64_image):
    r = requests.post(url='https://hf.space/embed/OFA-Sys/OFA-Image_Caption/+/api/predict/',
    json={"data":
    ["data:image/jpeg;base64,"+base64_image]
    })
    return r.json()

def upload_img(img, name):
    im_bytes = cv2.imencode(".jpg", img)[1].tobytes() #save to bucket
    put_in_bucket(name+'.jpg', im_bytes)

class Captioning(Resource):

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

        ################## Prediction
        outputs = {}
        for img_name in images_list:
            result = get_caption(data[img_name])
            outputs[img_name] = result["data"]
        
        ############################# Plotting boxes
        clear_bucket_images()

        #print(images_list)
        for img_name in images_list:
            #print(img_name)
            img = img_resize(data[img_name]) 
            #cv2.imwrite(filename=img_name+".jpg", img=img)
            upload_img(img, name=img_name)
        
        set_image_list(images=images_list)
        upload_notify(uid, "caption", outputs)
        
        #return jsonify(outputs)
        return jsonify(outputs)
