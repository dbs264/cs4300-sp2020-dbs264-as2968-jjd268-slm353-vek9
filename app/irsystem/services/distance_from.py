import certifi
import ssl
import math
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy import distance


def calc_distance(locA, locB):
    return distance.distance(locA, locB).miles


def add_distances(details, location_string):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(
        scheme='http', user_agent="clubadvisor", format_string="%s, New York City NY")
    pin = geolocator.geocode(location_string)
    pin_lat_lng = str(pin.latitude) + ", " + str(pin.longitude)

    for place in details:
        lat = place["geometry"]["location"]["lat"]
        lng = place["geometry"]["location"]["lng"]
        place_lat_lng = str(lat)+", "+str(lng)
        place["distance"] = calc_distance(pin_lat_lng, place_lat_lng)

    return details


def update_scores_for_distance(details):
    for place in details:
        place["score"] = place["score"]/math.log(place["distance"]+1.1)
