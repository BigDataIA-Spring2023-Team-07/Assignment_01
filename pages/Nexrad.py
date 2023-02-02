import streamlit as st

from backend import main



plt = main.plotNextRad("/home/dhanush/Big_data/Assignment_01/data/Nexrad.csv")
st.plotly_chart(plt)