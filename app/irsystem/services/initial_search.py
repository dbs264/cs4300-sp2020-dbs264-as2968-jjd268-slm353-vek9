import config, random, json, re
from collections import Counter
from app.irsystem.services import search_helpers as helpers


def random_five(details):
	for detail in details:
		detail["score"] = random.random()
	return helpers.sort_by_score(details)

def basic_search(details):
	for detail in details:
		if "rating" in detail and "user_ratings_total" in detail:
			detail["score"] = detail["rating"] * detail["user_ratings_total"]
		else:
			detail["score"] = 0
	return helpers.sort_by_score(details)

def keyword_search(details, word):
	for place in details:
		score = 0
		if "reviews" in place:
			for review in place["reviews"]:
				text = review["text"]
				if word in text:
					score += 1

		place["score"] = score
	return helpers.sort_by_score(details)

def multiple_key_word_counts(details, words):
	word_list = words.lower().split()
	for place in details:
		score = 0
		if "reviews" in place:
			for review in place["reviews"]:
				text_counter = Counter(review["text"].lower().split())
				for word in word_list:
					score += text_counter[word]
		place["score"] = score
	return helpers.sort_by_score(details)

def keyword_counts_normalized(details,words):
	word_list = words.lower().split()
	for place in details:
		score = 0
		denom = 1
		if "reviews" in place:
			for review in place["reviews"]:
				text_counter = Counter(re.findall(r'\w+',review["text"].lower()))
				for word in word_list:
					score += text_counter[word]
				denom += sum(text_counter.values())
		place["score"] = score/denom
	return helpers.sort_by_score(details)





def search_data(query, city):
	details = helpers.load_details(city)
	# top_five = multiple_key_word_counts(details, query)
	# top_five = random_five(details)
	top_five = keyword_counts_normalized(details, query)
	# print([[str(x["score"])] + x["reviews"] for x in top_five])
	return [helpers.format_output(x) for x in top_five]


	