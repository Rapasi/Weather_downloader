def weather_downnload(paikka):
  from cmath import nan
  import datetime as dt
  from xml.etree.ElementPath import prepare_self
  import math
  from fmiopendata.wfs import download_stored_query

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

  asema=(sorted(obs.data[latest_tstep].keys()))

  #print(obs.data[latest_tstep][asema[0]].keys())

  # Selecting observations 
  keys=['Air temperature','Wind speed','Wind direction','Snow depth','Pressure (msl)','Cloud amount']

  '''Converting values to a list of dictionarys which elements I know how to access. 
  there is likely easier way to do this, but this is what I was able to work out.'''

  arvot=[]
  for key in keys:
    values=obs.data[latest_tstep][asema[0]].get(key)
    arvot.append(values)
  # Converting to a dictionary and selecting values. 

  temperature=next(item for item in arvot if item["units"] == "degC")
  wind=next(item for item in arvot if item["units"] == "m/s")
  wind_direction=next(item for item in arvot if item["units"] == "deg")
  snow=next(item for item in arvot if item["units"] == "cm")
  pressure=next(item for item in arvot if item["units"] == "hPa")


  temp_value=temperature['value']
  wind_value=wind['value']
  pressure_value=pressure['value']
  snow_value=snow['value']
  wind_dir=wind_direction['value']

  # Checking if snow value is nan

  if math.isnan(snow_value):
    snow_value='ei saatavilla'


  # Listing weather observation from the nearest station. 
  value_list=[asema[0],temp_value,wind_value,wind_dir,pressure_value,snow_value]
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

def sea_download(location):
  from cmath import nan
  import datetime as dt
  from xml.etree.ElementPath import prepare_self
  import math
  from fmiopendata.wfs import download_stored_query

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
  asema=(sorted(obs.data[latest_tstep].keys()))
  

  values=obs.data[latest_tstep][str(location).capitalize()]
  for k, v in values.items():
    values=(k, v)
  sea_data=[list(values[1].values())[0],asema]
  return(sea_data)
  

if __name__=='__main__':
  pass