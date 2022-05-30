from utils.ai_platform_predict import call_model
from utils.get_api import get_endpoint, set_image_list
from flask_restful import Resource, reqparse
from flask import jsonify
from utils.img_convert import get_image_fromb64
import cv2
from utils.storage_code import put_in_bucket, clear_bucket_images
from utils.output_notify import upload_notify


def upload_img(img, name):
    im_bytes = cv2.imencode(".jpg", img)[1].tobytes() #save to bucket
    put_in_bucket(name+'.jpg', im_bytes)
    
def save_json(content, filename = "json_output.json"):
    with open(filename, 'w') as mreq:
        import json
        mreq.write(json.dumps(content))

def convert_output(outputs):
    converted = {}
    for output in outputs:
        converted[output["name"]] = output["detections"]
    return converted

def draw_box_resize(img_name, outputs, data):
    img = get_image_fromb64(data[img_name])
    #save_json(outputs, filename = "my_output.json")
    detections = outputs[img_name]
    for detection in detections:
        color = (255, 0, 0)
        thickness = 2
        start_point = (int(detection['xmin']), int(detection['ymin']))
        end_point = (int(detection['xmax']), int(detection['ymax']))
        text_pt = (int(detection["xmin"]), int(detection["ymin"])-10)
        cv2.putText(img, detection['name'], text_pt, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)
        cv2.rectangle(img, start_point, end_point, color, thickness)
        print(detection)
    img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    #img = cv2.resize(img, (int(w/1.2), int(h/1.2)), interpolation = cv2.INTER_AREA)
    img = cv2.resize(img, (1200, 900), interpolation = cv2.INTER_LINEAR)
    return img


class ObjectDetect(Resource):

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
        
        ################## JSON format conversion for Vertex AI prediction
        instance=[]
        for i in data.keys():
            if data[i] == None:
                continue
            temp = {}
            temp['name'] = i
            temp['image'] = data[i]
            instance.append(temp)
        model_input = {}
        model_input['instances'] = instance

        ################## Prediction
        outputs = call_model(model_input, "object")
        outputs = convert_output(outputs)
        ############################# Plotting boxes
        clear_bucket_images()

        for img_name in images_list:
            img = draw_box_resize(img_name, outputs, data) 
            upload_img(img, name=img_name)
        
        set_image_list(images=images_list)
        upload_notify(uid, "object", outputs)
        
        return jsonify(get_endpoint('object'))

"""
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
"""