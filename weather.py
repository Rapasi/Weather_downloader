from cmath import nan
import datetime as dt
from xml.etree.ElementPath import prepare_self
import math
from fmiopendata.wfs import download_stored_query
import requests
import json
import config
# Using api of finnish meteorological institute to download weather data

def weather_downnload(paikka):

  # Retrieve the latest hour of data from a bounding box
  end_time = dt.datetime.utcnow()
  start_time = end_time - dt.timedelta(minutes=60)
  print(start_time)
  # Convert times to properly formatted strings
  start_time = start_time.isoformat(timespec="seconds") + "Z"
  # -> 2020-07-07T12:00:00Z
  end_time = end_time.isoformat(timespec="seconds") + "Z"

  # Loading weather information 

  location=paikka
  obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                              args=['place=' + location + '&'
                                  "starttime=" + start_time,
                                    "endtime=" + end_time])

  latest_tstep = max(obs.data.keys())

  #print(dir(obs))
  #print(obs.data[latest_tstep])

  station=(sorted(obs.data[latest_tstep].keys()))

  #print(obs.data[latest_tstep][station[0]].keys())

  # Selecting observations 
  keys=['Air temperature','Wind speed','Wind direction','Snow depth','Pressure (msl)','Cloud amount']

  '''Converting values to a list of dictionarys which elements I know how to access. 
  there is likely easier way to do this, but this is what I was able to work out.'''

  value_list=[]
  for key in keys:
    values=obs.data[latest_tstep][station[0]].get(key)
    value_list.append(values)

  # Converting to a dictionary and selecting values. 

  temperature=value_list[0]['value']
  wind=value_list[1]['value']
  wind_direction=value_list[2]['value']
  snow=value_list[3]['value']
  pressure=value_list[4]['value']
  cloud=value_list[5]['units']
 


  

  # Checking if snow value is nan

  if math.isnan(snow):
    snow='ei saatavilla'


  # Listing weather observation from the nearest station. 
  value_list=[station[0],temperature,wind,wind_direction,pressure,snow,cloud]
  return(value_list)


# This function will convert wind direction to compass direction 
def degrees_to_cardinal(d):
    '''
    note: this is highly approximate...
    '''
    dirs = ["Pohjoisesta",  "Koillisesta",  "Idästä",  "Kaakosta", 
            "Etelästä",  "Lounaasta",  "Lännestä",  "Luoteesta"]
    ix = round(d / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

# a Function to round the wind direction to nearest 5.

def myround(x, base=5):
    return base * round(x/base)


# Same api as before but this time for sea level. Syntax is almost identical to weather download.

def sea_download(location):

  end_time = dt.datetime.utcnow()
  start_time = end_time - dt.timedelta(minutes=60)  

  # Retrieve the latest hour of data from a bounding box
  end_time = dt.datetime.utcnow()
  start_time = end_time - dt.timedelta(minutes=60)
  print(start_time)
  # Convert times to properly formatted strings
  start_time = start_time.isoformat(timespec="seconds") + "Z"
  # -> 2020-07-07T12:00:00Z
  end_time = end_time.isoformat(timespec="seconds") + "Z"

  obs = download_stored_query("fmi::forecast::oaas::sealevel::point::multipointcoverage",
                              args=["starttime=" + start_time,
                                    "endtime=" + end_time])

  latest_tstep = max(obs.data.keys())
  station=(sorted(obs.data[latest_tstep].keys()))
  

  values=obs.data[latest_tstep][str(location).capitalize()]
  for k, v in values.items():
    values=(k, v)
  sea_data=[list(values[1].values())[0],station]
  return(sea_data)
  

# Checkwx Api for metar data 

def metar_download(location):

  # INSERT YOUR API KEY HERE! YOU CAN GET ONE FROM checkwx.com. 

  hdr = {"X-API-Key": config.API_KEY}
  
  # Formating web address to take user input. 
  
  req = requests.get("https://api.checkwx.com/metar/{}".format(location), headers=hdr)

  # Json to dictionary and then to string. 
  
  try:
      req.raise_for_status()
      resp = json.loads(req.text)
      return resp['data'][0]

  except requests.exceptions.HTTPError as e:
      print(e)

if __name__=='__main__':
  pass