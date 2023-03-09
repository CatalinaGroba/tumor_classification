#comment
## Import external modules
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

# Import necessary functions for the API
from tumor_class.api.api_functions import resize_image
from tumor_class.ml_logic.registry import load_model
# Other imports
import numpy as np
from numpy import asarray
#import cv2
import io
import cv2
from PIL import Image

# Load FastApi Constructor, this will instanciate the API
app = FastAPI()

# Let's store the model into an app.state.model. This means that we don't have to download the model at every request from users but just once:
app.state.model = load_model()

# Decorator that sets up an endpoint for our API.
@app.get("/")
def index():
    return {"status": "ok"}

@app.post('/upload_image')

async def receive_image(img: UploadFile=File(...)):
    ### Receiving and decoding the image
    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = Image.fromarray(cv2_img)
    img = img.resize((256,256))
    np_img= np.array(img)

    #create again instance of the model and assert that it exists
    model = app.state.model

    # Load up the classes_dict to be to returned with a more descriptive label the prediction
    tumor_labels = {0: 'glioma_tumor', 1: 'meningioma_tumor', 2: 'pituitary_tumor', 3: 'no_tumor'}

    #Predict class
    prediction= model.predict(np.array([np_img]))

    #return tumor_label
    return {'prediction':tumor_labels[np.argmax(prediction)]}
