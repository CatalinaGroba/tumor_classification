# Import external modules
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

# Import necessary functions for the API
from api.api_functions import get_key_by_value, predict_class
# from taxifare.ml_logic.registry import load_model
# from model import predict
from TUMOR_CLASSIFICATION import jupyter

# Other imports
import numpy as np
import cv2
import io

# Load FastApi Constructor
app = FastAPI()

# load the models that we want to work with:
app.state.model = load_model()

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

    ### Load up the classes_dict to be to return with a more descriptive label the prediction
    model = app.state.model
    tumor_labels = {'0': 'glioma_tumor', '1': 'meningioma_tumor', '2': 'pituitary_tumor', '3': 'no_tumor'}
    return tumor_labels[str(model.predict(cv2_img))]


    ### Encoding and responding with the image
    im = cv2.imencode('.png', prediction)[1] # extension depends on which format is sent from Streamlit
    return Response(content=im.tobytes(), media_type="image/png")


@app.post('/test')
async def receive_image():
    ### Receiving and decoding the image
    prediction = predict_class('2')[0]
    print(f'prediction is {prediction}')
    ### Load up the classes_dict to be to return with a more descriptive label the prediction

    tumor_labels = {'0': 'glioma_tumor', '1': 'meningioma_tumor', '2': 'pituitary_tumor', '3': 'no_tumor'}
    return tumor_labels[str(model.predict(cv2_img)]
