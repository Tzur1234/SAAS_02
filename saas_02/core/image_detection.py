
### Initializing the imports
import numpy as np
import urllib
import json
import cv2
import os
from django.conf import settings

MEDIA_FOLDER = settings.MEDIA_ROOT
face_detector_file = 'haarcascade_frontalface_default.xml'
face_detector = os.path.join(MEDIA_FOLDER, face_detector_file)
print('face_detector: ', face_detector)


def detect_faces(image_path=None, url=None):
    #default value set to be false

    default = {"safely_executed": True} #because no detection yet

    # Image path that can be recognized for docker also

    if image_path:
               true_image_path = os.path.join(MEDIA_FOLDER, image_path.split('/media/')[1])
               image_to_read = read_image(path = true_image_path )
    elif url:
         image_to_read = read_image(url = url )
    else:
        default['error_value'] = 'no image was provided'
        default.update({"safely_executed": False})
        return default
          


    image_to_read = cv2.cvtColor(image_to_read, cv2.COLOR_BGR2GRAY)
    detector_value = cv2.CascadeClassifier(face_detector)
        #passing the face detector path
        # make sure to pass the complete path to the .xml file


    values = detector_value.detectMultiScale(image_to_read,
                                                scaleFactor=1.1,
                                                minNeighbors = 5,
                                                minSize=(30,30),
                                                flags = cv2.CASCADE_SCALE_IMAGE)

    ###dimensions for boxes that will pop up around the face
    values=[(int(a), int(b), int(a+c), int(b+d)) for (a,b,c,d) in values]

    default.update({"number_of_faces": len(values),
                    "faces":values,
                    "safely_executed": True })
    

    return default

def read_image(path=None, stream=None, url=None):

    ##### primarily URL but if the path is None
    ## load the image from your local repository

    if path is not None:
        image = cv2.imread(path)

    else:
        if url is not None:

            response = urllib.request.urlopen(url)

            data_temp = response.read()

        elif stream is not None:
            #implying image is now streaming
            data_temp = stream.read()

        image = np.asarray(bytearray(data_temp), dtype="uint8")

        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image










