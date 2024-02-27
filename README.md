
# Central API Repository  
## Description 
The Central API module serves as the intermediary linking the deep learning model servers and the Raspberry Pi in our system architecture. This repository encompasses code responsible for handling incoming requests, communicating with model servers, and dispatching push messages to Android application. The architecture follows a Flask-based REST API server, designed to receive JSON requests and provide JSON responses. 
## Directory Structure  -  
**/resources**: Contains the code executed when specific endpoints are triggered. 
## How It Works
 1. The API receives incoming requests from various sources. 2. Requests are forwarded to the model servers for processing. 3. Upon receiving model responses, the API sends push messages to connected Android devices. 
## Basic Setup  
1. Clone this repository to your local machine using `git clone`. 
2. Navigate to the `/resources` folder to explore endpoint-specific code. 
3. Ensure Flask and necessary dependencies are installed using `pip install -r requirements.txt`. 4. Run the Flask server with `python app.py`.

## How to deploy this repo
- Build the docker image using the  `Dockerfile`  in the repository, preferably using a service like Google Cloud Build to make the process easy.
- Deploy the model on Google Cloud Run service using the docker image that is built.
