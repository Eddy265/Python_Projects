import csv

#Import Nominatim and assign the google map API key 
from geopy.geocoders import Nominatim
key = "AIzaSyBjteltTAAJSi-m696Lbf5Ou3vhmhUZBLU"

geolocator = Nominatim(user_agent="key")

def get_lat_long(address):
  location = geolocator.geocode(address)
  if location is not None:
      return (location.latitude, location.longitude)
  return (None, None)

def save_to_csv(addresses):
  with open("lat_long.csv", "w") as csvfile:
    fieldnames = ["address", "latitude", "longitude"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for address in addresses:
      lat, long = get_lat_long(address)
      writer.writerow({"address": address, "latitude": lat, "longitude": long})
      
#Fetch the coordinate of the following addresses
addresses = ["City-Galerie Augsburg Willy-Brandt-Platz 1 86153 Augsburg", 
"Kurfürstendamm Kurfürstendamm 26 10719 Berlin", "Kö-Bogen Königsallee 2 40212 Düsseldorf",
"Große Bockenheimer Straße 30 60313 Frankfurt", "Jungfernstieg 12 20354 Hamburg"]
save_to_csv(addresses)
