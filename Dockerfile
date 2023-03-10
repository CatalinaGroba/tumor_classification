
# create a base image. Our image will inherit configurations and dependencies from this base image. Every addition will be built on top of this.
# For a python application for instance, it would be better to create a base image 'FROM python:3.9-slim-buster'... in our case weinherit all tensorflow library!
FROM tensorflow/tensorflow:latest

# copy all the requirements needed for users to run the application. It is written 2 times: the first one is the source(this directory)
# and the second one is the destination (docker container).
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

#which command do i run when i start?
CMD uvicorn tumor_class.api.api:app --host 0.0.0.0 --port $PORT
