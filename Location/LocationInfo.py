from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Brave")
location = geolocator.geocode("Istanbul")
print(location.address)
print((location.latitude, location.longitude))
(40.7410861, -73.9896297241625)
print(location.raw)
