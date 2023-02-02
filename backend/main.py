import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt


def plotNextRad(file_name):

    """
    This function plots the NEXRAD locations on a map based on the csv file
    Args:
        file_name (str): The name of the csv file
        Returns: None
    """


    df = pd.read_csv(file_name)
    df["Lon"] = -1 * df["Lon"]

    # Plot the NEXRAD locations on a map
    fig = px.scatter_geo(df,lat='Lat',lon='Lon')
    fig.update_layout(title = 'Nexrad Locations', title_x=0.5)

    return fig






