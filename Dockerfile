
# Create a base image. Our image will inherit configurations and dependencies from this base image. Every addition will be built on top of this.
# For a python application for instance, it would be better to create a base image 'FROM python:3.9-slim-buster'... in our case we want to inherit all tensorflow library!
# it is the case of almost every data science project.
FROM tensorflow/tensorflow:latest

# Copy all the requirements needed for users to run the application. It is written 2 times: the first one is the source(this directory)
# and the second one is the destination (docker container).
COPY requirements.txt requirements.txt

# Execute the install of latest version of pip and upgrade all packages that have dependencies with older versions of pip. It
# is important because all team members have this way the sameversion of pip and there will be no conflicts.
RUN pip install --upgrade pip

# install all the packages listed in the requirements.txt file.
RUN pip install -r requirements.txt

#Use the apt (advanced packing tool) to update all the last versions of all packages
RUN apt-get update

#Use the apt to install 3 ubuntu packages necessary for the video processing and dispaly within the docker image. The -y is for installing without user input.
RUN apt-get install \
  'ffmpeg'\
  'libsm6'\
  'libxext6'  -y


# Copy the folder tumor_class in the docker container. The / at the end means . take everything inside the folder
COPY tumor_class tumor_class/

# This specifies the command to run when the docker container starts. Uvicorn is the python web server, tumor_class is the application to be served. Finally, specify
# the host and port numbers that the server should listen to.
CMD uvicorn tumor_class.api.api:app --host 0.0.0.0 --port $PORT


# Once completed this file, in the terminal run these commands:
# --> 'docker build . -t eu.gcr.io/$GCP_PROJECT/$IMAGE' --> build the docker image, '.' means this directory,
# --> docker push eu.gcr.io/$GCP_PROJECT/$IMAGE

# the first line builds the docker file.
