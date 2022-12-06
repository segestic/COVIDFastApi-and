from io import BytesIO

import numpy as np
import tensorflow as tf
from PIL import Image
#from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.models import load_model
import os


model = None

def load_model2():
    model = load_model('application/models/resnet_ct.h5')
    #model = load_model(os.path.join(modelpath, 'resnet_ct.h5'))
    print("Model loaded")
    return model


def predict(image: Image.Image):
    global model
    if model is None:
        model = load_model2()

    image = np.asarray(image.resize((224, 224)))[..., :3]
    image = np.expand_dims(image, 0)
    image = image / 127.5 - 1.0

    result = model.predict(image)
    probability = result[0]
            #print("Resnet Predictions:")
    if probability[0] > 0.5:
        resnet_chest_pred = str('%.2f' % (probability[0]*100) + '% COVID') 
    else:
        resnet_chest_pred = str('%.2f' % ((1-probability[0])*100) + '% NonCOVID')

    response = []
    for i, res in enumerate(result):
        resp = {}
        resp["prediction"] = resnet_chest_pred
        #resp["confidence"] = f"{res[2]*100:0.2f} %"

        response.append(resp)

    return response


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image
