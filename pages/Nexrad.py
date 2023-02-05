import streamlit as st

from Assignment_01.backend import nexrad_main


st.title("Nexrad Locations")
plt = nexrad_main.plotNextRad("/home/dhanush/Big_data/Assignment_01/data/Nexrad.csv")
st.plotly_chart(plt)


st.title("Generate Link Nexrad")
