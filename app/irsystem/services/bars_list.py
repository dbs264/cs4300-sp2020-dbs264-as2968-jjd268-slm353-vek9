import config, random, json, re
from collections import Counter
from app.irsystem.services import search_helpers as helpers


def bars_list_for_city(city):
	return [x["name"] for x in helpers.load_details(city)]

	