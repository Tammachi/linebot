from pygeocoder import Geocoder
import googlemaps
import sys
import csv

args = sys.argv

googleapikey = 'AIzaSyB3wvto0C6bh_L-K0T5YvVInduXzrRGh24'
gmaps = googlemaps.Client(key=googleapikey)

data=[]
csvfile = "DSIGHT.csv"
fin = open(csvfile, "r",encoding="utf-8")
reader = csv.reader(fin)
for row in reader:
    data.append(row)
fin.close

result = []
for i in range(650):
    address = data[i][3]
    x = gmaps.geocode(address)
    result.append(x)
with open('localdata.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(result)
