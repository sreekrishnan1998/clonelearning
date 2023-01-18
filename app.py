
import streamlit as st
from objectDetection import *
from PIL import Image
from PIL.ExifTags import TAGS
from geopy.geocoders import Nominatim
import pandas as pd
import imageio
from tempfile import NamedTemporaryFile
from GPSPhoto import gpsphoto
import os
import folium
from st_aggrid import AgGrid
#detector = Detector(model_type='keypointsDetection')

import io

#detector.onVideo("pexels-tima-miroshnichenko-6388396.mp4")
#@st.cache
def func_1(x):
    detector = Detector(model_type=x)
    uploaded_files  = st.sidebar.file_uploader("UPLOAD INVOICE",type=['png','jpeg','jpg'], accept_multiple_files=True)
    for uploaded_file in uploaded_files:
      bytes_data = uploaded_file.read()
      img = Image.open(io.BytesIO(bytes_data))
      if uploaded_file is not None:
          st.write("**FileName :** ",uploaded_file.name)
          with st.expander("Show the Uploaded Invoice"):
              st.image(img, caption='Uploaded Image.')
      
          out=detector.onImage(uploaded_file.name)
          st.text(out)
          with st.expander("Proccesed Invoice"):
              with open(uploaded_file.name,mode = "wb") as f: 
                    f.write(uploaded_file.getbuffer())
              detector.onImage(uploaded_file.name)
              img_ = Image.open("result.jpg")
              st.image(img_, caption='Proccesed Image.')
        



def main():      
    def load_image(uploaded_file):
        img=Image.open(uploaded_file)
        return img
    st.title("INVOICE FORENSICS")
    image = Image.open(r"C:\Users\HARI\Desktop\allianz.png") 
    st.sidebar.image(image)
    #st.image(load_image(image_file))
    st.sidebar.header("APPROCHES")
    choice=st.sidebar.selectbox("SENARIOS",["Detection","Metadata Extraction"])
    if choice == "Detection":
        func_1('objectDetection')
    if choice == "Metadata Extraction":
      geolocator = Nominatim(user_agent="geoapiExercises")
      path = st.sidebar.file_uploader("Upload Image",type=['png','jpeg','jpg'])
      if path is not None:
          path_name=imageio.imread(path)
          with st.expander("**Uploaded Image**"):
              st.write("**FileName :** ",path.name)
              st.image(path_name)
              
          met_dat={**path_name.meta['EXIF_MAIN']}
          a=pd.DataFrame(met_dat.items())
          del met_dat['GPSInfo']
          i=range(1, len(met_dat) + 1)
          a=pd.DataFrame(met_dat.items(),index=i,columns=['Fields','Values'])
          a['Values'] = a['Values'].astype(str)
          AgGrid(a)


          with NamedTemporaryFile(dir='.',suffix='.jpg',delete=False) as f:
              f.write(path.getbuffer())
              gps=gpsphoto.getGPSData(f.name)
              lati=str(gps['Latitude'])
              lon=str(gps['Longitude'])
              st.write("**The GPS Coordinates are :**",(lati,lon))
              location = geolocator.reverse(lati+","+lon)
              st.write("**The location of the incident:**",location)
              coord=pd.DataFrame({"latitude":[float(lati)],"longitude":[float(lon)]})
              #st.text(coord)
              st.map(coord,zoom=15, use_container_width=False)
              
          os.remove(f.name)

      


if __name__ == '__main__':
		main()
