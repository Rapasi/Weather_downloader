from asyncio.windows_events import NULL
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

paikka='raahe'
obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=['place=' + paikka + '&'
                                "starttime=" + start_time,
                                  "endtime=" + end_time])
latest_tstep = min(obs.data.keys())
print(obs.data[latest_tstep])
print(sorted(obs.data[latest_tstep].keys()))
print(obs.data[latest_tstep]['Raahe Lapaluoto satama'].keys())

print(obs.data[latest_tstep]['Raahe Lapaluoto satama']['Air temperature'])