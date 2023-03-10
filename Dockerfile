
#create an image with the last version of  tensoflow image
FROM tensorflow/tensorflow:latest

#copy all the requirements needed for users to run the application
COPY requirements.txt requirements.txt

# execute the install of latest version of pip and upgrade all packages that have dependencies with older versions of pip. It
# is important because all team members have this way the sameversion of pip and there will be no conflicts.
RUN pip install --upgrade pip

# install all the requirements from the requirement file.
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install \
  'ffmpeg'\
  'libsm6'\
  'libxext6'  -y

COPY tumor_class tumor_class/

CMD uvicorn tumor_class.api.api:app --host 0.0.0.0 --port $PORT
