import config, random, json
from pathlib import Path

data_path = config.basedir+"/data/"



def load_details(city):
	city = city.lower().replace(" ", "_")
	with open(data_path+city+"_details.json") as f:
		return json.load(f)

def search_data(query, city):
	details = load_details(city)
	return random.sample(details,5)
	