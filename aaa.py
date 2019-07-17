from pygeocoder import Geocoder
import googlemaps
import sys

args = sys.argv

googleapikey = 'AIzaSyB3wvto0C6bh_L-K0T5YvVInduXzrRGh24'
gmaps = googlemaps.Client(key=googleapikey)
address = args[1]
result = gmaps.geocode(address)
print(result)
lat = result[0]["geometry"]["location"]["lat"]
lon = result[0]["geometry"]["location"]["lng"]
print ('緯度:'+str(lat)+' 経度:'+str(lon))
