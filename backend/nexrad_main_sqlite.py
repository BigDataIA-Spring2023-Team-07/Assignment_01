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
from pathlib import Path

load_dotenv()

base_path = os.environ.get('base_path')
data_path = os.environ.get('data_path')
data_path = os.path.join(base_path, data_path)

data_files = os.listdir(data_path)

database_file_name = os.path.join(data_path,'assignment_01.db')
database_file_path = os.path.join(data_path,database_file_name)



if 'assignment_01.db' not in data_files:
    file = os.path.join(data_path,'assignment_01.db')
    open(file, 'a').close()


def create_db(year):

    connection = sqlite3.connect(database_file_path)
    cursor = connection.cursor()
    if year == '2022':
        cursor.execute("Drop table if exists nexrad_2022")
        cursor.execute("Drop table if exists nexrad_2022_json")
        cursor.execute("Create table nexrad_2022 (Year text, Month text, Day text, Station text)")
        cursor.execute("Create table nexrad_2022_json (Json_file text)")

    if year == '2023':
        cursor.execute("Drop table if exists nexrad_2023")
        cursor.execute("Drop table if exists nexrad_2023_json")
        cursor.execute("Create table nexrad_2023 (Year text, Month text, Day text, Station text)")
        cursor.execute("Create table nexrad_2023_json (Json_file text)")

    connection.commit()
    connection.close()



def insert_data(year):
    
    df = pd.read_csv(os.path.join(data_path,'nexrad_data_' + year + '.csv'))
    create_db(year)
    connection = sqlite3.connect(database_file_path)
    cursor = connection.cursor()

    connection.commit()

    if year == '2022':
        for val in range(len(df)):
            cursor.execute("Insert into nexrad_2022 values (?,?,?,?)", (str(df.iloc[val]['Year']),str(df.iloc[val]['Month']), str(df.iloc[val]['Day']), df.iloc[val]['Station']))

        with open('/home/dhanush/Big_data/Assignment_01/data/nexrad_data_2022.json') as user_file:
            file_contents = user_file.read()
        data = json.loads(file_contents)

        data = json.dumps(data)
        cursor.execute("Insert into nexrad_2022_json values (?)", (data,))
        connection.commit()


    if year == '2023':
        for val in range(len(df)):
            cursor.execute("Insert into nexrad_2023 values (?,?,?,?)", (str(df.iloc[val]['Year']),str(df.iloc[val]['Month']), str(df.iloc[val]['Day']), df.iloc[val]['Station']))

        with open('/home/dhanush/Big_data/Assignment_01/data/nexrad_data_2023.json') as user_file:
            file_contents = user_file.read()
        data = json.loads(file_contents)

        data = json.dumps(data)
        cursor.execute("Insert into nexrad_2023_json values (?)", (data,))
        connection.commit()



