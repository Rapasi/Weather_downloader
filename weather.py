import datetime as dt

from fmiopendata.wfs import download_stored_query

# Retrieve the latest hour of data from a bounding box
end_time = dt.datetime.utcnow()
start_time = end_time - dt.timedelta(minutes=60)
print(start_time)
# Convert times to properly formatted strings
start_time = start_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T12:00:00Z
end_time = end_time.isoformat(timespec="seconds") + "Z"

#snd = download_stored_query("fmi::forecast::oaas::sealevel::point::multipointcoverage")

paikka=str(input('select place:'))
obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=['place=' + paikka + '&'
                                "starttime=" + start_time,
                                  "endtime=" + end_time])
latest_tstep = max(obs.data.keys())

#print(obs.data[latest_tstep])

asema=(sorted(obs.data[latest_tstep].keys()))

print(obs.data[latest_tstep][asema[0]].keys())

keys=['Air temperature','Wind speed','Wind direction','Snow depth','Pressure (msl)']
for key in keys:
  values=obs.data[latest_tstep][asema[0]].get(key)
  print(values.values())
print(asema)