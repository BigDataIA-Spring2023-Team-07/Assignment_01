import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import os
import boto3
from dotenv import load_dotenv
import json

load_dotenv()

def createConnection():
    
        """
        This function creates a connection to the AWS S3 bucket
        Args:
            None
        Returns:
            s3client (boto3.client): The boto3 client object
        """

        s3client = boto3.client('s3',
        region_name= "us-east-1",
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))

        return s3client

def createJson(year):
    """Creates a json file with the nexrad data

    Args:
        year (string): The year to be used to create the json file

    Returns:
        generatedJson (Json): Generated Json based on the fiven year
    """
    
    generatedJson = {}
    s3 = createConnection()

    bucket = 'noaa-nexrad-level2'
    result = s3.list_objects(Bucket=bucket, Prefix= year + "/" , Delimiter='/')
    
    for o in result.get('CommonPrefixes'):
        generatedJson[o.get('Prefix').split('/')[1]] = {}
    
    for m in list(generatedJson.keys()):
        result = s3.list_objects(Bucket=bucket, Prefix= year + "/" + m + '/' , Delimiter='/')
        for o in result.get('CommonPrefixes'):
            generatedJson[m][o.get('Prefix').split('/')[2]] = []

    for m in list(generatedJson.keys()):
        for d in list(generatedJson[m].keys()):
            result = s3.list_objects(Bucket=bucket, Prefix= year + '/' +m+'/'+d+'/', Delimiter='/')
            for o in result.get('CommonPrefixes'):
                generatedJson[m][d].append(o.get('Prefix').split('/')[3])

    return generatedJson




def grabData():

    year = ['2023', '2022']

    for y in year:
        with open('nexrad_data_'+str(y)+'.json', 'w') as outfile:
            json.dump(createJson(y), outfile)
  


def plotNextRad(file_name):

    """
    This function plots the NEXRAD locations on a map based on the csv file
    Args:
        file_name (str): The name of the csv file
        Returns: fig (plotly.graph_objects.Figure): The plotly figure object
    """


    df = pd.read_csv(file_name)
    df["Lon"] = -1 * df["Lon"]

    # Plot the NEXRAD locations on a map
    fig = px.scatter_geo(df,lat='Lat',lon='Lon')
    fig.update_layout(title = 'Nexrad Locations', title_x=0.5)

    return fig


if __name__ == '__main__':

    grabData()








