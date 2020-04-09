import requests, json

api_key = "AIzaSyDnrzcDEiBDwe0K5AM4whWb-Bp-38gql7w"
nearbyUrl ="https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
placeDetailsUrl ="https://maps.googleapis.com/maps/api/place/details/json?"
types =["bar","night_club"]

def build_place_id_list(file_name):
	locations = ["40.7233,-74.0030","40.7549,-73.9840","40.7675,-73.9758","40.6959,-73.9956","40.7265,73.9815","40.7150,73.9843","40.7118,74.0131","40.7336,74.0027","40.7396,74.0089","40.7501,74.0028","40.7629,73.9714"]
	locations += ["40.7813,73.9740","40.8075,73.9626","40.7662,73.9602","40.7081,73.9571","40.6734,74.0083","40.7213,73.9884","40.7460,73.9776","40.7423,73.9801"]
	radius = "10000"

	place_ids = set()

	for t in types:
		print("Type: " + t)
		for location in locations:
			print("Location: " + location)
		
			# r = requests.get(nearbyUrl+"key="+api_key+"&location="+location+"&radius="+radius+"&type="+t)
			r = requests.get(nearbyUrl+"key="+api_key+"&location="+location+"&rankby=distance"+"&type="+t)
			j = r.json()

			results = j["results"]
			for place in results:
				place_ids.add(place["place_id"])

			for i in range(2):
				if "next_page_token" in j:
					next_page_token = j["next_page_token"]
					r = requests.get(nearbyUrl+"key="+api_key+"&location="+location+"&radius="+radius+"&type="+t+"&pagetoken=" + next_page_token)
					j = r.json()
					while j["status"] == "INVALID_REQUEST":
						r = requests.get(nearbyUrl+"key="+api_key+"&location="+location+"&radius="+radius+"&type="+t+"&pagetoken=" + next_page_token)
						j = r.json()
					results = j["results"]
					for place in results:
						place_ids.add(place["place_id"])

	print(len(place_ids))


	with open(file_name, 'w') as outfile:
		json.dump(list(place_ids), outfile)

def open_place_id_list(file_name):
	with open (file_name) as f:
		place_ids = json.load(f)
		return place_ids

def call_place_details(place_id):
	fields = "name,url,price_level,user_ratings_total,rating,review/text,geometry/location,formatted_address," + \
		"formatted_phone_number,types"
	r = requests.get(placeDetailsUrl+"key="+api_key+"&place_id="+place_id+"&fields="+fields)
	return r.json()["result"]

def build_place_details_list(place_ids, file_name):
	places = []
	for id in place_ids:
		place = call_place_details(id)
		print(place["name"])
		places.append(place)

	
	with open(file_name, 'w') as outfile:
		json.dump(places, outfile)



def main():
	# build_place_id_list("place_ids.json") #ONLY RUN THIS IF YOU WANT TO WRITE OVER PLACE IDS
	# build_place_details_list(open_place_id_list("place_ids.json"),"place_details.json")
	build_place_id_list("by_radius_place_ids.json")
	# build_place_details_list(open_place_id_list("by_radius_place_ids.json"),"place_details.json")




if __name__ == '__main__':
	main()