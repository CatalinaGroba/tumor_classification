# Import external modules
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

# Import necessary functions for the API
from tumor_class.api.api_functions import get_key_by_value, load_model, predict_class, resize_image
# from taxifare.ml_logic.registry import load_model
# from model import predict
#from tumor_class.jupyter import load_model
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

    img = resize_image(img)

    # nparr = np.fromstring(contents, np.uint8)
    # cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray

    ### Load up the classes_dict to be to return with a more descriptive label the prediction
    model = app.state.model
    tumor_labels = {'0': 'glioma_tumor', '1': 'meningioma_tumor', '2': 'pituitary_tumor', '3': 'no_tumor'}
    #return tumor_labels[str(predict_class(img, model))]
    return model.predict()
