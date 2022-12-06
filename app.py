import streamlit as st
import json
import requests
from PIL import Image
import os


def load_image(image):
	img = Image.open(image)
	return img

def save_uploadedfile(uploadedfile):
     with open(os.path.join("images/img",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
         uploaded_location = os.path.join("images/img",uploadedfile.name)
     return uploaded_location#st.success("Saved File:{} to {}".format(uploadedfile.name, uploaded_location))
     

st.title("Covid Prediction App from CT Images")


#taking user inputs

st.write("")

#converting input to json


image = st.file_uploader("Upload CT Scan", type=["png","jpg","jpeg"])
 
if image is not None:
	  # To See details
	  file_details = {"filename":image.name, "filetype":image.type,
	      "filesize":image.size}
	  st.write(file_details)
	  #image1 = Image.open(image)
	  #img_array = np.array(image1)

	#View Uploaded Image
	  st.image(load_image(image),width=250)
	  #save image to disk
	  saved = save_uploadedfile(image)

	  if st.button ('Analyze'):
	  	  test_file = open(os.path.join("images/img", image.name), "rb")
	  	  response = requests.post('http://127.0.0.1:8000/predict/image', files={'file': test_file })
	  	  prediction = response.json()##json_object["prediction"]
	  	  st.write(prediction)
	  	  st. subheader (f"Response from Covid Analyzer API = {prediction}")

#RUN BOTH...
#streamlit run app.py
#uvicorn application.server.main:app 

#OPTION 2....



