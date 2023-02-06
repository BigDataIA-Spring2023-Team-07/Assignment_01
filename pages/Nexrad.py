import streamlit as st
import json
from backend import nexrad_main


st.title("Nexrad Locations")
plt = nexrad_main.plotNextRad("/home/dhanush/Big_data/Assignment_01/data/Nexrad.csv")
st.plotly_chart(plt)


st.title("Generate Link Nexrad")

yearSelected = st.selectbox(
    'Select the year',
    ('2022', '2023'))

if yearSelected == '2022':
    with open('/home/dhanush/Big_data/Assignment_01/data/nexrad_data_2022.json') as user_file:
        file_contents = user_file.read()
    data = json.loads(file_contents)

if yearSelected == '2023':
    with open('/home/dhanush/Big_data/Assignment_01/data/nexrad_data_2023.json') as user_file:
        file_contents = user_file.read()
    data = json.loads(file_contents)


monthSelected = st.selectbox(
    'Select the month',
    tuple(data.keys()))

daySelected = st.selectbox(
    'Select the day',
    tuple(data[monthSelected].keys()))

stationSelected = st.selectbox(
    'Select the station',
    tuple(data[monthSelected][daySelected]))

file_tup = nexrad_main.listFiles(yearSelected, monthSelected, daySelected, stationSelected)
fileSelected = st.selectbox(
        'Select the file',
        file_tup)


if st.button("Submit"):
    if fileSelected == None:
        st.warning('Please click on the submit button and then select the file before clicking on generate link', icon="⚠️")
    else:
        generated_url = nexrad_main.generateLink(yearSelected, monthSelected, daySelected, stationSelected, fileSelected)
        st.markdown("**Public URL**")
        st.write(generated_url)


        st.markdown("**AWS S3 URL**")
        obj_key = nexrad_main.getKey(yearSelected, monthSelected, daySelected, stationSelected, fileSelected)
        user_key = nexrad_main.uploadFiletoS3(obj_key, 'noaa-nexrad-level2', 'damg7245-team7')
        user_url = nexrad_main.generateUserLink('damg7245-team7' ,user_key)
        st.write(user_url)





