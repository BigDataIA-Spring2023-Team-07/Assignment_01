import re
import requests
from datetime import datetime


# base_goes_url = "https://noaa-goes18.s3.amazonaws.com/"
base_nexrad_url = "https://noaa-nexrad-level2.s3.amazonaws.com/"
format = "%Y%m%d%H%M%S"
pattern = "^(?:[A-Z]{4}\d{8}|[A-Z]{3}\d{9})_\d{6}(?:_V\d{2}\.gz|_V\d{2}_MDM|_V\d{2}|\.gz)$"



def get_nexrad_file_url(filename):

  if re.match(pattern, filename):

    date_time_val = filename.split('_')[0][4:12]+filename.split('_')[1][0:6]


    if date_time_format(date_time_val):

      year = filename.split('_')[0][4:8]
      month_of_year = filename.split('_')[0][8:10]
      day_of_month = filename.split('_')[0][10:12]
      ground_station_id = filename.split('_')[0][0:4]
      # timestamp = filename.split('_')[1]

      final_url = base_nexrad_url + year + '/' + month_of_year + '/' + day_of_month + '/' + ground_station_id + '/' + filename
      # print(final_url)

      try:
        # Make a GET request to the URL
        response = requests.get(final_url)

        # Check if the response was successful
        if response.status_code == 200:
           return final_url
        else:
           return response.status_code

      except Exception as e:
        return e

    else:
      return 'invalid datetime'

  else:
    return 'invalid filename'


def date_time_format(val):

  res = True
  
  try:
    res = bool(datetime.strptime(val, format))
  except ValueError:
    res = False
  return res