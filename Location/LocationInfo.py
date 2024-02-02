from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geocoder
import time

# GPS verilerini almak için kullanılacak bir fonksiyon
def get_current_location():
    try:
        # Geocoder ile anlık konumu al
        location = geocoder.ip('me').latlng
        return location
    except GeocoderTimedOut:
        # Zaman aşımı hatası durumunda tekrar deneyin
        return get_current_location()

# GPS koordinatlarını adres bilgisine çevirmek için kullanılacak bir fonksiyon
def get_address_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="Brave")
    location = geolocator.reverse((latitude, longitude), language="en")
    return location.address

while True:
    # Anlık konum bilgisi al
    current_location = get_current_location()
    print("Current Location:")
    print("Latitude:", current_location[0])
    print("Longitude:", current_location[1])

    # GPS koordinatlarını adres bilgisine çevir
    address = get_address_from_coordinates(current_location[0], current_location[1])
    print("Address:", address)

    # Belirli bir süre bekleyerek tekrar konum bilgisi alınmasını sağla
    time.sleep(60)  # Örneğin, 60 saniye (1 dakika) aralıklarla konum almayı sağlar.
