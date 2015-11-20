


from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.reverse("43.706625,-72.2890706")
addr = location.address.encode("ascii", "replace")
 
addr = addr.replace(',', ';')
print addr
 
print ','.join(['testing', addr])

# from geopy.geocoders import GoogleV3
# geolocator = GoogleV3()
# location = geolocator.reverse("44.3530470,-72.7400562", exactly_one=True)
# print location
# print location.address

 
