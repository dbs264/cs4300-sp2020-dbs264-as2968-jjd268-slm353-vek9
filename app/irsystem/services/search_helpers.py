import config, random, json


data_path = config.basedir+"/data/"

def format_output(place_details):
	result = {"score":place_details["score"]}
	if "name" in place_details:
		result["name"] = place_details["name"]
	else: 
		result["name"] = ""
	if "formatted_address" in place_details:
		result["address"] = place_details["formatted_address"]
	else: 
		result["address"] = ""
	if "formatted_phone_number" in place_details:
		result["phone_number"] = place_details["formatted_phone_number"]
	else: 
		result["phone_number"] = ""
	if "geometry" in place_details and "location" in place_details["geometry"]:
		result["coordinates"] = place_details["geometry"]["location"]
	else: 
		result["coordinates"] = {"lat": "", "lng" :  ""}
	if "opening_hours" in place_details and "weekday_text" in place_details["opening_hours"]:
		result["hours_open"] = place_details["opening_hours"]["weekday_text"]
	else: 
		result["hours_open"] = []
	if "price_level" in place_details:
		result["price"] = place_details["price_level"]
	else: 
		result["price"] = ""
	if "rating" in place_details:
		result["rating"] = place_details["rating"]
	else: 
		result["name"] = ""
	if "reviews" in place_details:
		result["reviews"] = [x["text"] for x in place_details["reviews"]]
	else:
		result["reviews"] = []
	if "user_ratings_total" in place_details:
		result["num_ratings"] = place_details["user_ratings_total"]
	else:
		result["num_ratings"] = ""
	if "url" in place_details:
		result["google_url"] = place_details["url"]
	else:
		result["google_url"] = ""
	result["photo_url"] = place_details["photo_url"]
	return result

def load_details(city):
	city = city.lower().replace(" ", "_")
	with open(data_path+city+"_details.json") as f:
		return json.load(f)

def sort_by_score(list,k =5):
	return sorted(list, key = lambda x: x["score"],reverse = True)[:k]



	