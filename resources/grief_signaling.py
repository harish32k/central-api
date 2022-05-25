from flask_restful import Resource, reqparse
from flask import jsonify
import cv2
import PIL.Image as Image
import numpy as np
import base64
import imghdr
import smtplib
import ssl
from email.message import EmailMessage
import os

def get_image_fromb64(encoded_str):
    im_bytes = base64.b64decode(encoded_str)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    imageBGR = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
    return imageRGB


imgdir = "temp_captures"

def create_dir_clear():
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)
    dir = os.path.join(imgdir)
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

class GriefSignaling(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, required = True ,help="please enter uid") #uid can be the token or user id
        parser.add_argument('img1', type=str, required = False ,help="please enter img1")
        parser.add_argument('img2', type=str, required = False ,help="please enter img2")
        parser.add_argument('img3', type=str, required = False ,help="please enter img3")
        parser.add_argument('img4', type=str, required = False ,help="please enter img4")
        parser.add_argument('lat', type=str, required = False ,help="please enter latitude")
        parser.add_argument('lon', type=str, required = False ,help="please enter longitude")
        data = parser.parse_args()
        
        img1 = data["img1"]; img2 = data["img2"]; img3 = data["img3"]; img4 = data["img4"]
        if (img1 == img2 == img3 == img4 == None):
            return {"message" : "please send atleast one image"}, 400

        uid = data.pop("uid") 
        lat = data.pop("lat")
        lon = data.pop("lon")

        create_dir_clear()

        images_list = [] #create a list of images sent to the API
        for key in data:
            if(data[key]):
                images_list.append(key)
        images_list.sort()
        print(images_list)
        files=[]
        for img_name in images_list:
            image = get_image_fromb64(data[img_name])
            temp = Image.fromarray(image)
            imgpath = os.path.join(imgdir, img_name+".jpg")
            temp.save(imgpath)
            files.append(imgpath)
        msg = EmailMessage()
        msg.set_content("The body of the email is here")
        msg["Subject"] = "Grief Signaling"
        msg["From"] = "vimpaired.app@gmail.com"
        msg["To"] = "harish.akula213@gmail.com"
        msg.set_content(f"""Emergency for the user.\n  \
        User: {uid}
        \n Latitude:{lat} , Longitide: {lon}\n
        Open in google maps:\
        https://www.google.com/maps/search/?api=1&query={lat},{lon}""")
        for file in files:
            with open(file, 'rb') as m:
                file_date = m.read()
                file_type = imghdr.what(m.name)
                file_name = m.name
            msg.add_attachment(file_date, maintype='image', subtype=file_type, filename=file_name)

        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
            smtp.starttls(context=context)
            smtp.login(msg["From"], "Vimpaired2021")
            smtp.send_message(msg)

        return jsonify("Grief Signaling Successful")