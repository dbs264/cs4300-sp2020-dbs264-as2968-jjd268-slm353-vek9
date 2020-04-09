import requests, json

api_key = "AIzaSyDnrzcDEiBDwe0K5AM4whWb-Bp-38gql7w"


def main():
	placeUrl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
	inp = "subway"
	inpType = "textquery"
	midtown = "circle:1000@40.7549,-73.9840"
	soho = "circle:10000@40.7233,-74.0030"


	nearbyUrl ="https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
	sohoLocation = "40.7233,-74.0030"
	radius = "500"
	bar = "bar"
	night_club = "night_club"
	restuarant = "restuarant"


	# r = requests.get(placeUrl+"key="+api_key+"&input="+inp+"&inputtype="+inpType+"&locationbias"+soho+"&fields=name,rating")

	r1 = requests.get(nearbyUrl+"key="+api_key+"&location="+sohoLocation+"&radius="+radius+"&type="+night_club)

	listofPlaces = r1.json()

	onePlaceId = listofPlaces["results"][1]['place_id']
	onePlaceName = listofPlaces["results"][1]['name']

	placeDetailsUrl ="https://maps.googleapis.com/maps/api/place/details/json?"

	r2 = requests.get(placeDetailsUrl+"key="+api_key+"&place_id="+onePlaceId+"&fields=rating,review/text")

	singlePlaceResult = r2.json()

	print(onePlaceName)
	print()
	print(singlePlaceResult)


	# for item in x["results"]:

	# 	print()
	# 	print(item)























if __name__ == '__main__':
	main()