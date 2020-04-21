import requests, json

api_key = "AIzaSyDnrzcDEiBDwe0K5AM4whWb-Bp-38gql7w"
nearbyUrl ="https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
placeDetailsUrl ="https://maps.googleapis.com/maps/api/place/details/json?"
photosUrl = "https://maps.googleapis.com/maps/api/place/photo?"
types =["bar","night_club"]
radius = "10000"
data_path = "../data/"

def write_lat_long_pairs(city,locations):
	with open((data_path+city+"/"+city+"_coordinates.json"), 'w') as outfile:
		json.dump(locations, outfile)

def read_lat_long_pairs(city):
	with open(data_path+city+"/"+city+"_coordinates.json") as coords:
		return json.load(coords)

def build_place_id_list(locations, city,existing_place_ids=[]):
	place_ids = set(existing_place_ids)
	print(city +  ": ")
	for t in types:
		print("Type: " + t)
		for location in locations:
			print("Location: " + location)
		
			# r = requests.get(nearbyUrl+"key="+api_key+"&location="+location+"&radius="+radius+"&type="+t)
			r = requests.get(nearbyUrl+"key="+api_key+"&location="+location+"&rankby=distance"+"&type="+t)
			j = r.json()
			if len(j["results"] )==0:
				print(j)

			results = j["results"]
			for place in results:
				place_ids.add(place["place_id"])

			for i in range(2):
				if "next_page_token" in j:
					next_page_token = j["next_page_token"]
					r = requests.get(nearbyUrl+"key="+api_key+"&location="+city+"&radius="+radius+"&type="+t+"&pagetoken=" + next_page_token)
					j = r.json()
					while j["status"] == "INVALID_REQUEST":
						r = requests.get(nearbyUrl+"key="+api_key+"&location="+location+"&radius="+radius+"&type="+t+"&pagetoken=" + next_page_token)
						j = r.json()
					results = j["results"]
					for place in results:
						place_ids.add(place["place_id"])

	print("There are {} establishments in {}!".format(len(place_ids),city))


	with open((data_path+city+"/"+city+"_place_ids.json"), 'w') as outfile:
		json.dump(list(place_ids), outfile)

def open_place_id_list(city):
	with open (data_path+city+"/"+city+"_place_ids.json") as f:
		place_ids = json.load(f)
		return place_ids

def add_to_place_ids(city,locations,isNewCity = False):
	if isNewCity:
		place_ids = []
		write_lat_long_pairs(city,locations)
	else:
		place_ids = open_place_id_list(city)
		write_lat_long_pairs(city,(locations+read_lat_long_pairs(city)))
	build_place_id_list(locations,city,place_ids)

	
def convert_photos(detail):
	if "photos" in detail and len(detail["photos"]) > 0:
		photoRef = detail["photos"][0]["photo_reference"]
		detail["photo_url"] = photosUrl+"key="+api_key+"&photoreference="+photoRef+"&maxwidth=1000"
	else:
		detail["photo_url"] = "https://www.cs.cornell.edu/~cristian/index_files/IMG_1820_3.jpg"
	return detail


def call_place_details(place_id):
	fields = "name,url,price_level,user_ratings_total,rating,review/text,geometry/location,formatted_address," + \
		"formatted_phone_number,types,opening_hours,photos"
	r = requests.get(placeDetailsUrl+"key="+api_key+"&place_id="+place_id+"&fields="+fields)
	return convert_photos(r.json()["result"])



def build_place_details_list(city):
	print("Building {} place details file".format(city))
	place_ids = open_place_id_list(city)
	places = []
	count = 0
	for i in place_ids:
		place = call_place_details(i)
		places.append(place)
		count += 1

		if count%(len(place_ids)//20) == 0:
			print("{0:.0%} built".format((count/len(place_ids))))

	
	with open(data_path+city+"/"+city+"_details.json", 'w') as outfile:
		json.dump(places, outfile)



def main():
	# add_to_place_ids("new_york",["40.755678,-73.983963"])
	build_place_details_list("new_york")
	return



if __name__ == '__main__':
	main()