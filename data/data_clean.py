import numpy as np 
import json

def convert_city(city_name):
    with open(city_name, 'r') as f:
        data = json.load(f)
    return data

data = convert_city('data/new_york_details.json')

keys = ['formatted_address', 'formatted_phone_number', 'geometry', 'name', 'opening_hours', 'price_level', 
        'rating', 'reviews', 'types', 'url', 'user_ratings_total']

print(data[0]['opening_hours'])

for place in data:
        if 'geometry' in place:
            place['geometry'] = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
        if 'opening_hours' in place: place['opening_hours'] = place['opening_hours']['weekday_text']
        if 'reviews' in place:
            reviews = []
            for review in place['reviews']:
                reviews.append(review['text'])
            place['reviews'] = reviews

print(data[0]['opening_hours'])
