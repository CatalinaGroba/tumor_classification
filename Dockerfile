FROM tensorflow/tensorflow:latest

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install \
  'ffmpeg'\
  'libsm6'\
  'libxext6'  -y

COPY tumor_class tumor_class/

CMD uvicorn tumor_class.api.api:app --host 0.0.0.0 --port $PORT
