#!/usr/bin/python3

import sys
#import geoip2.webservice
print (sys.argv[1])

#print str(sys.argv[1])
import geoip2.database
import socket 

print(socket.gethostname())

reader = geoip2.database.Reader('/Shared/nginx/GeoLite2-City.mmdb')
response = reader.city(str(sys.argv[1]))

Lat = response.location.latitude
ISO = response.country.iso_code
Long = response.location.longitude
State = response.subdivisions.most_specific.name
City = response.city.name
Country = response.country.name
Zip = response.postal.code
IP = str(sys.argv[1])
Domain = str(sys.argv[2])
duration = int(sys.argv[3])
print (Country)
print (State)
print (City)
print (Zip)
print (Long)
print (Lat)
print (ISO)
print (IP)
reader.close()


import datetime
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "USERNAME"
ifpass = "PASSWORD"
ifdb   = "Docker"
ifhost = "192.168.0.1"
ifport = "8081"
hostname = socket.gethostname()
measurement_name = ("ReverseProxyConnections")
print (measurement_name)
# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": time,
        "tags": {
            "key": ISO,
            "latitude": Lat,
            "longitude": Long,
            "Domain": Domain,
            "IP": IP
            },
        "fields": {
            "Domain": Domain,
            "latitude": Lat,
            "longitude": Long,
            "State": State,
            "City": City,
            "key": ISO,
            "IP": IP,
            "name": Country,
            "duration": duration,
            "metric": 1
        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
ifclient.write_points(body)

