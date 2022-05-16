import cv2
import numpy as np
import base64

def get_image_fromb64(encoded_str):
    im_bytes = base64.b64decode(encoded_str)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    imageBGR = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)
    return imageRGB


def get_b64_fromimage(image):
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    retval, buffer = cv2.imencode('.png', image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return jpg_as_text