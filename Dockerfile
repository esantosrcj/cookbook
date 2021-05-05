# syntax=docker/dockerfile:1

# base image for application
FROM python:3.9-slim

# use this path as the default location for all subsequent commands
WORKDIR /app

# copy the requirements.txt file into the working directory /app
COPY requirements.txt requirements.txt

# execute command to install into the image
RUN pip3 install -r requirements.txt

# add source code into the image
COPY . .

# command to run after image is executed inside the container
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]