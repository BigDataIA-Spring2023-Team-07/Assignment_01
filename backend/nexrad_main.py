import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import os
import boto3
from dotenv import load_dotenv
import json
import random, string
import logging
import sqlite3

logging.basicConfig(filename = 'assignment_01.log',level=logging.INFO, force= True, format='%(asctime)s:%(levelname)s:%(message)s')




load_dotenv()

base_path = os.environ.get('base_path')
data_path = os.environ.get('data_path')
data_path = os.path.join(base_path, data_path)


database_file_name = os.path.join(data_path,'assignment_01.db')
ddl_file_name = os.path.join(data_path,'assignment_01.sql')


def createConnection():
    
    """ This function creates a connection to the AWS S3 bucket
    Args:
        None
    Returns:
        s3client (boto3.client): The boto3 client object
    """

    s3client = boto3.client('s3',
    region_name= "us-east-1",
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))

    logging.info("Connection to S3 bucket created")

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
    paginator = s3.get_paginator('list_objects')
    config = {"PageSize":100}
    operation_parameters = {'Bucket': bucket,
                        'Prefix': year + "/",
                        'Delimiter':'/',
                        'PaginationConfig': config}
                        

    result = paginator.paginate(**operation_parameters)

    for page in result:
        for o in page.get('CommonPrefixes'):
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

    """Grabs the data from the S3 bucket and creates a json file for each year"""

    # Call grab data function to create Json for year 2022 and 2023

    year = ['2022', '2023']

    for y in year:

        data_files = os.listdir(data_path)
        if 'nexrad_data_'+str(y)+'.json' not in data_files:
            with open(os.path.join(data_path, 'nexrad_data_'+str(y)+'.json'), 'w') as outfile:
                json.dump(createJson(y), outfile)
                logging.info("Json file created for the year " + str(y))

    


def listFiles(year, month, day, station):

    """Lists the files in the S3 bucket baswed on the given year, month, day and station

    Args:
        year (str): year chosen by the user
        month (str): month chosen by the user
        day (str): day chosen by the user
        station (str): station chosen by the user

    Returns:
        tuple: Returns the tuple list of all the files available for the given year, month, day and station
    """

    s3 = createConnection()
    lst = []
    bucket = 'noaa-nexrad-level2'
    result = s3.list_objects(Bucket=bucket, Prefix= year + "/" + month + "/" + day + "/" + station + "/", Delimiter='/')
    for o in result.get('Contents'):
        lst.append(o.get('Key').split('/')[4])

    logging.info("files retrieved for the given year, month, day and station from the S3 bucket")
    return tuple(lst) 

def getKey(year, month, day, station, file):

    """Gets the key of the file in the S3 bucket"""
    
    s3 = createConnection()
    bucket = 'noaa-nexrad-level2'
    result = s3.list_objects(Bucket=bucket, Prefix= year + "/" + month + "/" + day + "/" + station + "/" , Delimiter='/')
    for o in result.get('Contents'):
        if file in o.get('Key'):
            return (o.get('Key'))



def uploadFiletoS3(key, source_bucket, target_bucket):

    """Uploads the file to the S3 bucket

    Args:
        key (str): The key of the file
        source_bucket (str): source bucket name
        target_bucket (str): target bucket name

    Returns:
        str: Returns the key of the uploaded file
    """
    
    s3 = boto3.resource('s3',
         aws_access_key_id= os.environ.get('AWS_ACCESS_KEY'),
         aws_secret_access_key= os.environ.get('AWS_SECRET_KEY')
    )
    copy_source = {
        'Bucket': source_bucket,
        'Key': key
    }
    uploaded_key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    s3.meta.client.copy(copy_source, target_bucket , uploaded_key)

    logging.info("File uploaded to the S3 bucket from source destination to target destination")
    return uploaded_key


def generateUserLink(bucket_name, key):
    """Generates the user link in public s3 bucket

    Args:
        bucket_name (str): name of the user bucket
        key (str): Key name of the file

    Returns:
        str: Returns the url of the file
    """

    url = "https://" + bucket_name + ".s3.amazonaws.com" + "/" + key
    logging.info("link generated for the Nexxrad bucket")
    return url



def generateLink(year, month, day, station, file):

    """Generates the link for the file in the nexrad S3 bucket
    
    Args:
        year (str): year chosen by the user
        month (str): month chosen by the user
        day (str): day chosen by the user
        station (str): station chosen by the user
        file (str): file chosen by the user
        
    Returns:
        str: Returns the url of the file"""



    url = "https://noaa-nexrad-level2.s3.amazonaws.com/" + year + "/" + month + "/" + day + "/" + station + "/" + file

    logging.info("link generated for the User bucket")
    logging.info(url)
    return url


def generateCsv(year):


    month_lst = []
    day_lst = []
    station_lst = []


    with open('/home/dhanush/Big_data/Assignment_01/data/nexrad_data_' + year + '.json') as user_file:
        file_contents = user_file.read()
    data = json.loads(file_contents)


    for month in data:
        for day in data[month]:
            month_lst.append(month)
            day_lst.append(day)
            station_lst.append(data[month][day])

    df = pd.DataFrame({'Year': year, 'Month': month_lst, 'Day': day_lst, 'Station': station_lst})
    df.to_csv(os.path.join(data_path, 'nexrad_data_' + year + '.csv'), index=False)



    


def plotNextRad(file_name):

    """
    This function plots the NEXRAD locations on a map based on the csv file
    Args:
        file_name (str): The name of the csv file
    Returns:
        fig (plotly.graph_objects.Figure): The plotly figure object
    """

    df = pd.read_csv(file_name)
    df["Lon"] = -1 * df["Lon"]

    # Plot the NEXRAD locations on a map
    fig = px.scatter_geo(df,lat='Lat',lon='Lon')
    fig.update_layout(title = 'Nexrad Locations', title_x=0.5)

    return fig

