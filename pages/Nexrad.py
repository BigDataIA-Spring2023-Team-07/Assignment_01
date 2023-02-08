import streamlit as st
import json
from backend import nexrad_main, nexrad_main_sqlite
import os

# st.title("Nexrad Locations")
# plt = nexrad_main.plotNextRad("/home/dhanush/Big_data/Assignment_01/data/Nexrad.csv")
# st.plotly_chart(plt)


base_path = os.environ.get('base_path')
data_path = os.environ.get('data_path')
data_path = os.path.join(base_path, data_path)

st.title("Generate Link Nexrad")


# Grabs the Json if its not available
nexrad_main.grabData()

# Creates csv file based on the Json

data_files = os.listdir(data_path)
if 'nexrad_data_2022.csv' not in data_files:
    nexrad_main.generateCsv('2022')

if 'nexrad_data_2023.csv' not in data_files:
    nexrad_main.generateCsv('2023')

# Inserts the contents from csv file to db
year = ['2022','2023']
for y in year:
    nexrad_main_sqlite.insert_data(y)


# User selects the year
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





# User selects the month
monthSelected = st.selectbox(
    'Select the month',
    tuple(data.keys()))

# User selects the day
daySelected = st.selectbox(
    'Select the day',
    tuple(data[monthSelected].keys()))


# User selects the station
stationSelected = st.selectbox(
    'Select the station',
    tuple(data[monthSelected][daySelected]))


# User selects the file
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





