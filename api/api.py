# Import external modules
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

# Import necessary functions for the API
from api.api_functions import get_key_by_value, predict_class
# from model import predict

# Other imports
import numpy as np
import cv2
import io


app = FastAPI()

# Allow all requests (optional, good for development purposes)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],  # Allows all origins
                   allow_credentials=True,
                   allow_methods=["*"],  # Allows all methods
                   allow_headers=["*"],  # Allows all headers
                    )

@app.get("/")
def index():
    return {"status": "ok"}

@app.post('/upload_image')
async def receive_image(img: UploadFile=File(...)):
    ### Receiving and decoding the image
    contents = await img.read()

    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray

    ### Do cool stuff with your image.... For example face detection
    prediction = predict_class(cv2_img)

    ### Load up the classes_dict to be to return with a more descriptive label the prediction
    classes_dict = {'glioma_tumor':0,'meningioma_tumor':1,'pituitary_tumor':2,'no_tumor':3}

    return get_key_by_value(classes_dict, str(prediction))

    ### Encoding and responding with the image
    im = cv2.imencode('.png', prediction)[1] # extension depends on which format is sent from Streamlit
    return Response(content=im.tobytes(), media_type="image/png")
