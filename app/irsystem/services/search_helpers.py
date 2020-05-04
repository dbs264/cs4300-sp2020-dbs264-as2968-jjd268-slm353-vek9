import config
import random
import json
import re
from nltk_data.corpora import wordnet
from nltk.tokenize import TreebankWordTokenizer


data_path = config.basedir+"/data/"

tokenizer = TreebankWordTokenizer()

with open(data_path + "stopwords.json") as f:
    stop_words = json.load(f)


def format_output(place_details):
    result = {"score": place_details["score"]}
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
        result["coordinates"] = {"lat": "", "lng":  ""}
    if "opening_hours" in place_details and "weekday_text" in place_details["opening_hours"]:
        result["hours_open"] = format_dates(place_details["opening_hours"]["weekday_text"])
    else:
        result["hours_open"] = []
    if "price_level" in place_details:
        result["price"] = int(place_details["price_level"])
    else:
        result["price"] = 1
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
    if "distance" in place_details:
        result["distance"] = place_details["distance"]
    else:
        result["distance"] = 0
    return result


def load_details(city):
    city = city.lower().replace(" ", "_")
    with open(data_path+city+"/"+city+"_details.json") as f:
        return json.load(f)


def load_meta_data(city):
    city = city.lower().replace(" ", "_")
    with open(data_path+city+"/"+city+"_meta_data.json") as f:
        return json.load(f)


def load_details_with_clusters(city):
    city = city.lower().replace(" ", "_")
    with open(data_path+city+"/"+city+"_details_with_clusters.json") as f:
        return json.load(f)


def sort_by_score(list, k=10):
    return sorted(list, key=lambda x: x["score"], reverse=True)[:k]


def filter_by_attributes(details, price, cluster=None):
    if cluster:
        return list(filter(lambda x: (int(x["price_level"]) <= price and x["cluster"] == cluster) if "price_level" in x else False, details))
    else:
        return list(filter(lambda x: int(x["price_level"]) <= price if "price_level" in x else False, details))

def format_dates(hours_open):
    new = {}
    for e in hours_open:
       day = re.search("^[^:]*", e).group().strip()
       times = re.search("(?<=:).*", e).group().strip()
       new[day]=times
    return new

def query_expansion(query):
    query_tokens = tokenizer.tokenize(query.lower()) 
    query_tokens = [i for i in query_tokens if not i in stop_words]
    synonyms = []
    for word in query_tokens:
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        synonyms.append(word)
    return set(synonyms)