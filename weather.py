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

  print(obs.data[latest_tstep][asema[0]].keys())

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
  cloud_amount=arvot[-1]['units']
  print(cloud_amount)

  # This function will convert wind direction to compass direction 

  def degrees_to_cardinal(d):
      '''
      note: this is highly approximate...
      '''
      dirs = ["Pohjoisesta",  "Koillisesta",  "Idästä",  "Kaakosta", 
              "Etelästä",  "Lounaasta",  "Lännestä",  "Luoteesta"]
      ix = round(d / (360. / len(dirs)))
      return dirs[ix % len(dirs)]


  # Checking if snow value is nan

  if math.isnan(snow_value):
    snow_value='ei saatavilla'

  # a Function to round the wind direction to nearest 5.

  def myround(x, base=5):
      return base * round(x/base)

  # Printing out current wether in nearest station to location. 

  return(f"{asema[0]}\n\n"
        f"Lämpötila {temp_value}\u00b0C\n"
        f'Tuuli {wind_value} m/s {degrees_to_cardinal(wind_dir) } ({myround(wind_dir)}\u00b0)\n'
        f'Lumen syvyys {snow_value}\n'
        f'Ilmanpaine {pressure_value} hPa'
        )
  
if __name__=='__main__':
  pass