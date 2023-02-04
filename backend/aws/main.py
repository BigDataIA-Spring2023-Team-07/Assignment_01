import os
import boto3
import logging
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=LOGLEVEL,
    datefmt='%Y-%m-%d %H:%M:%S')

s3client = boto3.client('s3',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )

# def list_files_in_user_bucket():
#     logging.debug("fetching objects in user s3 bucket")
#     my_bucket = s3client.list_objects(Bucket=os.environ.get('USER_BUCKET_NAME'))
#     files = my_bucket.get('Contents')
#     logging.info("Printing Files in User bucket")
#     for file in files:
#         print('\t' * 4 + file['Key'])


def list_files_in_noaa_bucket():
    logging.debug("fetching objects in NOAA s3 bucket")
    paginator = s3client.get_paginator('list_objects_v2')
    noaa_bucket = paginator.paginate(Bucket='noaa-goes18', PaginationConfig={"PageSize": 50})
    logging.info("Writing Files in list from NOAA bucket")
    station=[]
    year=[]
    day=[]
    hour=[]
    
    for count, page in enumerate(noaa_bucket):
        files = page.get("Contents")
        for file in files:
            
            if 'ABI-L1b-RadC' not in file['Key'].split("/")[0]:
                break
            
            # if ((file['Key'].split("/")[0] not in station) or (file['Key'].split("/")[1] not in year) or (file['Key'].split("/")[2] not in day) or (file['Key'].split("/")[3] not in hour)):
            station.append(file['Key'].split("/")[0])
            year.append(file['Key'].split("/")[1])
            day.append(file['Key'].split("/")[2])
            hour.append(file['Key'].split("/")[3])
            print(file['Key'])
        else:
            continue
        break
        
    df_goes18=pd.DataFrame({'Station': station,
     'Year': year,
     'Day': day,
     'Hour': hour
    })
    df_goes18.drop_duplicates(inplace=True)
    df_goes18.to_csv('df_goes18.csv',index=False)    


def main():
    # return
    # list_files_in_user_bucket()
    list_files_in_noaa_bucket()


if __name__ == "__main__":
    logging.info("Script starts")
    main()
    logging.info("Script ends")