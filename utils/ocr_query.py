from cProfile import label
import os
import cv2
#from opencv_resizer import ResizeWithAspectRatio
#from json_opener import data
import base64
from google.cloud.vision_v1 import AnnotateImageResponse
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'tokens/project-vimpaired-889c1c6eb1c1.json'

def detect_text(content):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        
    response_json = AnnotateImageResponse.to_dict(response)
    return response_json

def convert_json(results):
    #u_results = []
    for text in results[1:]:
        vertices = ([(vertex["x"], vertex["y"])
                    for vertex in text["bounding_poly"]["vertices"]])
        text["coordinates"] = vertices
        #u_results.append(text)
    #return u_results
    return results

def draw_boxes(img, results):
    for text in results[1:]:
        label = text["description"]
        color = (255, 0, 255) # Blue color in BGR
        thickness = 3 # Line thickness of 3 px
        isClosed = True
        vertices = text["coordinates"]
        img = cv2.polylines(img, np.int32([vertices]), isClosed, color, thickness)
        x1, y1 = vertices[0][0], vertices[0][1]
        cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    return img

def get_text_from_image(base64_img):

    #decode base64 image to bytes for prediction
    #base64_img = images_dict["img2"]
    base64_img_bytes = base64_img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)

    #prediction
    print("requesting OCR ...")
    response = detect_text(decoded_image_data)
    print("Success!")

    #convert image into opencv format for drawing boxes
    nparr = np.frombuffer(decoded_image_data, np.uint8)
    img = img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    window_name = 'Image'
    results = response["text_annotations"]
    results = convert_json(results)
    img = draw_boxes(img, results)
    #resize = ResizeWithAspectRatio(img, width=650) # Resize by width OR
    #cv2.imshow(window_name, resize) 
    #cv2.waitKey(5000)
    #cv2.imwrite('new_output.png', img)
    return img, results

if __name__ == '__main__':
    #get_text_from_image(data)
    pass